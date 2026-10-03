from src.equipment.cell_factory import CNCCellFactory, CNCInspection
from src.equipment.equipment_base import Inspection
from src.equipment.equipment_service import EquipmentService
from src.equipment.inspection_decorators import (
    LoggedInspection,
    TimedInspection,
)
from src.production.prod_order import StandardOrder


class FakeLogger:
    def __init__(self):
        self.records = []

    def log(self, message, level="INFO"):
        self.records.append((level, message))


class FailingInspection(Inspection):
    def inspect(self, order) -> bool:
        return False


def make_order():
    return StandardOrder("OP-1", "Pieza A", 10)


def test_decorated_inspection_keeps_the_inspection_interface():
    decorated = LoggedInspection(CNCInspection(), logger=FakeLogger())
    assert isinstance(decorated, Inspection)


def test_logged_inspection_logs_start_and_approval():
    logger = FakeLogger()
    inspection = LoggedInspection(CNCInspection(), logger=logger)

    result = inspection.inspect(make_order())

    assert result is True
    assert [level for level, _ in logger.records] == ["INFO", "INFO"]
    assert "OP-1" in logger.records[0][1]
    assert "aprobada" in logger.records[1][1]


def test_logged_inspection_warns_when_inspection_fails():
    logger = FakeLogger()
    inspection = LoggedInspection(FailingInspection(), logger=logger)

    result = inspection.inspect(make_order())

    assert result is False
    assert logger.records[-1][0] == "WARNING"
    assert "rechazada" in logger.records[-1][1]


def test_timed_inspection_measures_duration_with_injected_clock():
    ticks = iter([10.0, 10.5])
    inspection = TimedInspection(CNCInspection(), clock=lambda: next(ticks))

    assert inspection.last_duration is None
    assert inspection.inspect(make_order()) is True
    assert inspection.last_duration == 0.5


def test_decorators_can_be_stacked_and_keep_the_result():
    logger = FakeLogger()
    ticks = iter([1.0, 3.0])
    timed = TimedInspection(FailingInspection(), clock=lambda: next(ticks))
    inspection = LoggedInspection(timed, logger=logger)

    assert inspection.inspect(make_order()) is False
    assert timed.last_duration == 2.0
    assert logger.records[-1][0] == "WARNING"


def test_equipment_service_works_with_decorated_inspection():
    service = EquipmentService(CNCCellFactory())
    logger = FakeLogger()
    service.inspection = LoggedInspection(service.inspection, logger=logger)

    assert service.run_inspection(make_order()) is True
    assert len(logger.records) == 2
