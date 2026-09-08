from src.equipment.cell_factory import CNCCellFactory, RobotCellFactory
from src.equipment.equipment_service import EquipmentService


def test_service_never_mixes_families():
    service = EquipmentService(CNCCellFactory())
    assert type(service.equipment).__name__ == "CNCMachine"
    assert type(service.inspection).__name__ == "CNCInspection"

    service2 = EquipmentService(RobotCellFactory())
    assert type(service2.equipment).__name__ == "RobotArm"
    assert type(service2.inspection).__name__ == "RobotInspection"


def test_start_and_stop_change_status():
    service = EquipmentService(CNCCellFactory())
    service.start_machine()
    assert service.equipment.status == "Operando"
    service.stop_machine()
    assert service.equipment.status == "Parada"