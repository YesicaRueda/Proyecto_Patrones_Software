

from src.equipment.production_line import ProductionLine
from src.equipment.equipment_service import EquipmentService
from src.equipment.cell_factory import CNCCellFactory, RobotCellFactory


def test_line_starts_and_stops_all_units():
    line = ProductionLine("Línea Norte")
    cnc = EquipmentService(CNCCellFactory())
    robot = EquipmentService(RobotCellFactory())

    line.add_unit(cnc)
    line.add_unit(robot)

    line.start()
    assert cnc.status() == "Operando"
    assert robot.status() == "Operando"

    line.stop()
    assert cnc.status() == "Parada"
    assert robot.status() == "Parada"


def test_line_status_returns_all_unit_statuses():
    line = ProductionLine("Línea Norte")
    cnc = EquipmentService(CNCCellFactory())
    line.add_unit(cnc)

    cnc.start()
    assert line.status() == ["Operando"]