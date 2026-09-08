from src.equipment.cell_factory import (
    CNCCellFactory,
    RobotCellFactory,
    CNCMachine,
    CNCInspection,
    RobotArm,
    RobotInspection,
)


def test_cnc_factory_creates_cnc_products():
    factory = CNCCellFactory()
    assert isinstance(factory.create_equipment(), CNCMachine)
    assert isinstance(factory.create_inspection(), CNCInspection)


def test_robot_factory_creates_robot_products():
    factory = RobotCellFactory()
    assert isinstance(factory.create_equipment(), RobotArm)
    assert isinstance(factory.create_inspection(), RobotInspection)


def test_factory_never_mixes_families():
    expected_family = {
        CNCMachine: CNCInspection,
        RobotArm: RobotInspection,
    }

    for factory in [CNCCellFactory(), RobotCellFactory()]:
        equipment = factory.create_equipment()
        inspection = factory.create_inspection()
        expected_inspection_type = expected_family[type(equipment)]

        assert isinstance(inspection, expected_inspection_type)