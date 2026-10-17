import pytest

from src.equipment.equipment_service import EquipmentService
from src.equipment.cell_factory import CNCCellFactory
from src.facade.mes_facade import MESFacade
from src.production.prod_order import StandardOrder, UrgentOrder
from src.production.prod_service import ProductionService
from src.production.prod_service_proxy import ProductionServiceProxy


class FakeLogger:
    def __init__(self):
        self.records = []

    def log(self, message, level="INFO"):
        self.records.append((level, message))


def make_proxy(rol, service=None, logger=None, usuario="ana"):
    service = service or ProductionService()
    return ProductionServiceProxy(
        service, usuario, rol, logger=logger or FakeLogger()
    )


def test_unknown_role_is_rejected():
    with pytest.raises(ValueError):
        ProductionServiceProxy(ProductionService(), "ana", "invitado")


def test_supervisor_can_run_the_full_flow_on_the_real_service():
    service = ProductionService()
    proxy = make_proxy("supervisor", service)

    proxy.add_order(StandardOrder("OP-1", "Pieza A", 10))
    proxy.start_order("OP-1")
    proxy.complete_order("OP-1")

    assert service.get_order("OP-1").status == "Completada"


def test_operator_cannot_register_orders():
    service = ProductionService()
    proxy = make_proxy("operador", service)

    with pytest.raises(PermissionError):
        proxy.add_order(StandardOrder("OP-1", "Pieza A", 10))

    assert service.get_order("OP-1") is None


def test_operator_can_start_and_complete_orders():
    service = ProductionService()
    service.add_order(StandardOrder("OP-1", "Pieza A", 10))
    proxy = make_proxy("operador", service)

    proxy.start_order("OP-1")
    proxy.complete_order("OP-1")

    assert service.get_order("OP-1").status == "Completada"


def test_operator_can_start_with_equipment():
    service = ProductionService()
    service.add_order(StandardOrder("OP-1", "Pieza A", 10))
    equipment = EquipmentService(CNCCellFactory())
    equipment.start_machine()
    proxy = make_proxy("operador", service)

    proxy.start_order_with_equipment("OP-1", equipment)

    assert service.get_order("OP-1").status == "En producción"


def test_read_only_role_can_query_but_not_change_anything():
    service = ProductionService()
    service.add_order(StandardOrder("OP-1", "Pieza A", 10))
    service.add_order(UrgentOrder("OP-2", "Pieza B", 5))
    proxy = make_proxy("consulta", service)

    assert proxy.get_order("OP-1") is service.get_order("OP-1")
    assert [o.order_id for o in proxy.get_pending_queue()] == ["OP-2", "OP-1"]
    assert dict(proxy.orders) == service.orders

    with pytest.raises(PermissionError):
        proxy.start_order("OP-1")

    with pytest.raises(PermissionError):
        proxy.complete_order("OP-1")

    assert service.get_order("OP-1").status == "Pendiente"


def test_orders_view_is_read_only():
    service = ProductionService()
    service.add_order(StandardOrder("OP-1", "Pieza A", 10))
    proxy = make_proxy("consulta", service)

    with pytest.raises(TypeError):
        proxy.orders["OP-2"] = StandardOrder("OP-2", "Pieza B", 5)

    assert list(service.orders) == ["OP-1"]


def test_denied_attempts_are_audited_and_logged_as_warning():
    logger = FakeLogger()
    proxy = make_proxy("consulta", logger=logger, usuario="visita")

    with pytest.raises(PermissionError):
        proxy.add_order(StandardOrder("OP-1", "Pieza A", 10))

    assert proxy.audit == [{
        "usuario": "visita",
        "rol": "consulta",
        "operacion": "add_order",
        "detalle": "OP-1",
        "permitido": False,
    }]
    assert logger.records[-1][0] == "WARNING"
    assert "visita" in logger.records[-1][1]


def test_allowed_writes_are_audited_but_reads_are_not():
    logger = FakeLogger()
    proxy = make_proxy("supervisor", logger=logger, usuario="ana")

    proxy.add_order(StandardOrder("OP-1", "Pieza A", 10))
    proxy.get_order("OP-1")
    proxy.get_pending_queue()
    proxy.orders

    assert [r["operacion"] for r in proxy.audit] == ["add_order"]
    assert proxy.audit[0]["permitido"] is True
    assert len(logger.records) == 1
    assert logger.records[0][0] == "INFO"
    assert "ana" in logger.records[0][1]


def test_errors_of_the_real_service_are_not_hidden():
    proxy = make_proxy("supervisor")
    proxy.add_order(StandardOrder("OP-1", "Pieza A", 10))

    with pytest.raises(ValueError):
        proxy.add_order(StandardOrder("OP-1", "Pieza B", 5))

    with pytest.raises(ValueError):
        proxy.start_order("NO-EXISTE")


def test_real_service_still_works_without_the_proxy():
    service = ProductionService()
    make_proxy("consulta", service)

    service.add_order(StandardOrder("OP-1", "Pieza A", 10))
    service.start_order("OP-1")

    assert service.get_order("OP-1").status == "En producción"


def test_facade_works_with_a_supervisor_proxy():
    proxy = make_proxy("supervisor")
    mes = MESFacade(production_service=proxy)

    mes.register_order("F-1", "Pieza A", 10)

    assert mes.process_order("F-1") is True
    assert mes.get_status_report()["ordenes"]["Completada"] == 1


def test_facade_with_operator_proxy_cannot_register_but_can_operate():
    service = ProductionService()
    service.add_order(StandardOrder("F-1", "Pieza A", 10))
    mes = MESFacade(production_service=make_proxy("operador", service))

    with pytest.raises(PermissionError):
        mes.register_order("F-2", "Pieza B", 5)

    assert mes.process_order("F-1") is True


def test_facade_with_read_only_proxy_can_only_report():
    service = ProductionService()
    service.add_order(StandardOrder("F-1", "Pieza A", 10))
    mes = MESFacade(production_service=make_proxy("consulta", service))

    assert mes.get_status_report()["total_ordenes"] == 1

    with pytest.raises(PermissionError):
        mes.run_order("F-1")

    assert service.get_order("F-1").status == "Pendiente"
