from datetime import datetime

import pytest

from src.equipment.cell_factory import CNCCellFactory, RobotCellFactory
from src.equipment.equipment_base import Inspection
from src.equipment.inspection_decorators import LoggedInspection
from src.facade.mes_facade import MESFacade
from src.production.order_group import OrderGroup
from src.production.prod_order import StandardOrder, UrgentOrder


class FailingInspection(Inspection):
    def inspect(self, order) -> bool:
        return False


class FakeLogger:
    def __init__(self):
        self.records = []

    def log(self, message, level="INFO"):
        self.records.append((level, message))


def test_register_order_creates_standard_order_by_default():
    mes = MESFacade()

    order = mes.register_order("F-1", "Pieza A", 10)

    assert isinstance(order, StandardOrder)
    assert mes.production.get_order("F-1") is order


def test_register_order_creates_urgent_order_with_builder_data():
    mes = MESFacade()
    entrega = datetime(2026, 10, 30)

    order = mes.register_order(
        "F-1",
        "Pieza A",
        10,
        urgent=True,
        lote="L-1",
        fecha_entrega=entrega,
        equipo_asignado="CNC-01",
    )

    assert isinstance(order, UrgentOrder)
    assert order.lote == "L-1"
    assert order.fecha_entrega == entrega
    assert order.equipo_asignado == "CNC-01"


def test_register_order_rejects_duplicate_id():
    mes = MESFacade()
    mes.register_order("F-1", "Pieza A", 10)

    with pytest.raises(ValueError):
        mes.register_order("F-1", "Pieza B", 5)


def test_register_batch_registers_a_single_group():
    mes = MESFacade()

    group = mes.register_batch(
        "LOTE-1", "L-1", [("F-1", "Pieza A", 10), ("F-2", "Pieza B", 20)]
    )

    assert isinstance(group, OrderGroup)
    assert group.quantity == 30
    assert group.count_orders() == 2
    assert mes.production.get_order("LOTE-1") is group
    assert mes.production.get_order("F-1") is None
    assert all(child.lote == "L-1" for child in group.children)


def test_register_batch_rejects_empty_items():
    mes = MESFacade()

    with pytest.raises(ValueError):
        mes.register_batch("LOTE-1", "L-1", [])

    assert mes.production.get_order("LOTE-1") is None


def test_register_batch_registers_nothing_when_an_item_is_invalid():
    mes = MESFacade()

    with pytest.raises(ValueError):
        mes.register_batch(
            "LOTE-1", "L-1", [("F-1", "Pieza A", 10), ("F-1", "Pieza B", 5)]
        )

    assert mes.production.get_order("LOTE-1") is None


def test_run_order_starts_the_cell_automatically():
    mes = MESFacade()
    mes.register_order("F-1", "Pieza A", 10)
    assert mes.equipment.equipment.status == "Parada"

    mes.run_order("F-1")

    assert mes.equipment.equipment.status == "Operando"
    assert mes.production.get_order("F-1").status == "En producción"


def test_run_order_unknown_order_raises():
    mes = MESFacade()

    with pytest.raises(ValueError):
        mes.run_order("NO-EXISTE")


def test_stop_cell_stops_equipment():
    mes = MESFacade()
    mes.start_cell()

    mes.stop_cell()

    assert mes.equipment.equipment.status == "Parada"


def test_finish_order_completes_when_inspection_is_approved():
    mes = MESFacade()
    mes.register_order("F-1", "Pieza A", 10)
    mes.run_order("F-1")

    assert mes.finish_order("F-1") is True
    assert mes.production.get_order("F-1").status == "Completada"


def test_finish_order_keeps_order_in_production_when_inspection_fails():
    mes = MESFacade()
    mes.equipment.inspection = FailingInspection()
    mes.register_order("F-1", "Pieza A", 10)
    mes.run_order("F-1")

    assert mes.finish_order("F-1") is False
    assert mes.production.get_order("F-1").status == "En producción"


def test_finish_order_rejects_order_that_is_not_in_production():
    mes = MESFacade()
    mes.register_order("F-1", "Pieza A", 10)

    with pytest.raises(ValueError):
        mes.finish_order("F-1")

    with pytest.raises(ValueError):
        mes.finish_order("NO-EXISTE")


def test_process_order_runs_the_complete_flow():
    mes = MESFacade()
    mes.register_order("F-1", "Pieza A", 10)

    assert mes.process_order("F-1") is True
    assert mes.production.get_order("F-1").status == "Completada"


def test_process_order_on_a_batch_completes_all_children():
    mes = MESFacade()
    group = mes.register_batch(
        "LOTE-1", "L-1", [("F-1", "Pieza A", 10), ("F-2", "Pieza B", 20)]
    )

    assert mes.process_order("LOTE-1") is True
    assert group.status == "Completada"
    assert all(child.status == "Completada" for child in group.children)


def test_status_report_summarizes_equipment_and_orders():
    mes = MESFacade()
    mes.register_order("F-1", "Pieza A", 10, urgent=True)
    mes.register_order("F-2", "Pieza B", 5)
    mes.register_order("F-3", "Pieza C", 5)
    mes.process_order("F-3")

    report = mes.get_status_report()

    assert report["equipo"] == "CNCMachine"
    assert report["estado_equipo"] == "Operando"
    assert report["total_ordenes"] == 3
    assert report["ordenes"] == {
        "Pendiente": 2,
        "En producción": 0,
        "Completada": 1,
    }
    assert report["cola_pendiente"] == [
        {"order_id": "F-1", "prioridad": 10},
        {"order_id": "F-2", "prioridad": 1},
    ]


def test_facade_works_with_another_equipment_family():
    mes = MESFacade(RobotCellFactory())
    mes.register_order("F-1", "Pieza A", 10)

    assert mes.process_order("F-1") is True
    assert mes.get_status_report()["equipo"] == "RobotArm"


def test_facade_keeps_subsystems_accessible():
    mes = MESFacade(CNCCellFactory())

    assert mes.production is not None
    assert mes.equipment.factory.__class__ is CNCCellFactory


def test_facade_works_with_decorated_inspection():
    mes = MESFacade()
    logger = FakeLogger()
    mes.equipment.inspection = LoggedInspection(
        mes.equipment.inspection, logger=logger
    )
    mes.register_order("F-1", "Pieza A", 10)

    assert mes.process_order("F-1") is True
    assert len(logger.records) == 2
