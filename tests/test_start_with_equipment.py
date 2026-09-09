import pytest
from src.production.prod_service import ProductionService
from src.production.order_builder import OrderBuilder
from src.production.prod_factory import UrgentOrderCreator
from src.equipment.equipment_service import EquipmentService
from src.equipment.cell_factory import CNCCellFactory


def test_start_order_fails_if_equipment_not_operating():
    production = ProductionService()
    equipment = EquipmentService(CNCCellFactory())  # nunca se llama start_machine()

    data = OrderBuilder("OP-200", "Pieza X", 1).build()
    order = UrgentOrderCreator().create_order(data)
    production.add_order(order)

    with pytest.raises(ValueError):
        production.start_order_with_equipment("OP-200", equipment)


def test_start_order_succeeds_if_equipment_operating():
    production = ProductionService()
    equipment = EquipmentService(CNCCellFactory())
    equipment.start_machine()

    data = OrderBuilder("OP-201", "Pieza Y", 1).build()
    order = UrgentOrderCreator().create_order(data)
    production.add_order(order)

    production.start_order_with_equipment("OP-201", equipment)

    assert production.get_order("OP-201").status == "En producción"