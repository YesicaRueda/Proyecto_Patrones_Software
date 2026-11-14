import pytest

from src.commands.invoker import CommandInvoker
from src.commands.mes_commands import ProcessOrderCommand
from src.equipment.cell_factory import CNCCellFactory
from src.equipment.equipment_base import Inspection
from src.observer.observable_facade import ObservableMESFacade
from src.observer.observer import EventType, MESEvent, Observer, Subject
from src.observer.observers import ProductionMetricsObserver, RejectionAlertObserver
from src.production.prod_service import ProductionService
from src.production.prod_service_proxy import ProductionServiceProxy


class FakeLogger:
    def __init__(self):
        self.records = []

    def log(self, message, level="INFO"):
        self.records.append((level, message))


class Recorder(Observer):
    def __init__(self):
        self.events = []

    def update(self, event):
        self.events.append(event)

    @property
    def types(self):
        return [e.type for e in self.events]


class Exploding(Observer):
    def update(self, event):
        raise RuntimeError("boom")


class RejectingInspection(Inspection):
    def inspect(self, order):
        return False


class FakeClock:
    def __init__(self, t=0.0):
        self.t = t

    def __call__(self):
        return self.t


def ev(type_, t=0.0, order_id=None, **data):
    return MESEvent(type_, t, order_id, data)


def make_mes(**kwargs):
    kwargs.setdefault("logger", FakeLogger())
    return ObservableMESFacade(CNCCellFactory(), **kwargs)


# ---------------------------------------------------------------- Subject
def test_attach_rejects_non_observer():
    with pytest.raises(TypeError):
        Subject().attach(object())


def test_notify_delivers_to_all_in_order():
    subject, a, b = Subject(logger=FakeLogger()), Recorder(), Recorder()
    subject.attach(a)
    subject.attach(b)
    subject.notify(ev(EventType.ORDER_STARTED, order_id="X"))
    assert a.types == b.types == [EventType.ORDER_STARTED]


def test_filter_by_event_type():
    subject, rec = Subject(logger=FakeLogger()), Recorder()
    subject.attach(rec, [EventType.INSPECTION_REJECTED])
    subject.notify(ev(EventType.ORDER_STARTED))
    subject.notify(ev(EventType.INSPECTION_REJECTED))
    assert rec.types == [EventType.INSPECTION_REJECTED]


def test_detach_stops_delivery_and_unknown_raises():
    subject, rec = Subject(logger=FakeLogger()), Recorder()
    subject.attach(rec)
    subject.detach(rec)
    subject.notify(ev(EventType.ORDER_STARTED))
    assert rec.events == []
    with pytest.raises(ValueError):
        subject.detach(rec)


def test_duplicate_and_invalid_subscriptions_rejected():
    subject, rec = Subject(), Recorder()
    subject.attach(rec)
    with pytest.raises(ValueError):
        subject.attach(rec)
    with pytest.raises(ValueError):
        Subject().attach(Recorder(), ["NO_EXISTE"])
    with pytest.raises(ValueError):
        Subject().attach(Recorder(), [])


def test_failing_observer_does_not_stop_others_and_is_logged():
    logger = FakeLogger()
    subject, rec = Subject(logger=logger), Recorder()
    subject.attach(Exploding())
    subject.attach(rec)
    subject.notify(ev(EventType.ORDER_STARTED))
    assert rec.types == [EventType.ORDER_STARTED]
    assert logger.records[0][0] == "WARNING"
    assert "Exploding" in logger.records[0][1]


def test_event_is_immutable():
    event = MESEvent(EventType.ORDER_STARTED, 1.0, "X")
    with pytest.raises(Exception):
        event.type = "OTRO"
    with pytest.raises(TypeError):
        event.data["x"] = 1


# -------------------------------------------------------------- Observers
def test_metrics_counts_and_quality():
    m = ProductionMetricsObserver()
    m.update(ev(EventType.ORDER_STARTED, order_id="A", quantity=10))
    m.update(ev(EventType.INSPECTION_APPROVED, order_id="A", quantity=10))
    m.update(ev(EventType.ORDER_COMPLETED, order_id="A", quantity=10))
    m.update(ev(EventType.INSPECTION_REJECTED, order_id="B", quantity=10))
    assert m.orders_started == 1 and m.orders_completed == 1
    assert m.units_completed == 10
    assert (m.inspections_approved, m.inspections_rejected) == (1, 1)
    assert m.quality_rate() == 0.5


def test_metrics_operating_time_and_availability():
    m = ProductionMetricsObserver()
    m.update(ev(EventType.CELL_STARTED, 10.0))
    m.update(ev(EventType.CELL_STOPPED, 40.0))
    m.update(ev(EventType.CELL_STARTED, 60.0))
    assert m.operating_seconds() == 30.0
    assert m.operating_seconds(now=70.0) == 40.0
    # ventana 10 -> 110 = 100 s; operativo = 30 + (110 - 60) = 80 s
    assert m.availability(now=110.0) == pytest.approx(0.8)
    assert m.cell_starts == 2


def test_metrics_without_data_returns_none():
    m = ProductionMetricsObserver()
    assert m.quality_rate() is None
    assert m.availability(now=5.0) is None


def test_alert_observer_records_only_rejections():
    logger = FakeLogger()
    alerts = RejectionAlertObserver(logger=logger)
    alerts.update(ev(EventType.ORDER_STARTED, order_id="A"))
    alerts.update(ev(EventType.INSPECTION_REJECTED, 3.0, "B"))
    assert alerts.alerts == (("B", 3.0),)
    assert logger.records == [
        ("WARNING", "ALERTA: inspección rechazada para la orden B")
    ]


# ------------------------------------------------- ObservableMESFacade
def test_process_order_publishes_full_sequence():
    mes, rec = make_mes(), Recorder()
    mes.attach(rec)
    mes.register_order("O-1", "Pieza", 10)
    assert mes.process_order("O-1") is True
    assert rec.types == [
        EventType.CELL_STARTED,
        EventType.ORDER_STARTED,
        EventType.INSPECTION_APPROVED,
        EventType.ORDER_COMPLETED,
    ]
    assert rec.events[1].order_id == "O-1"
    assert rec.events[1].data["quantity"] == 10


def test_rejected_inspection_publishes_rejection_and_no_completion():
    mes, rec = make_mes(), Recorder()
    mes.attach(rec)
    mes.equipment.inspection = RejectingInspection()
    mes.register_order("O-2", "Pieza", 5)
    assert mes.process_order("O-2") is False
    assert EventType.INSPECTION_REJECTED in rec.types
    assert EventType.ORDER_COMPLETED not in rec.types


def test_cell_events_are_not_duplicated():
    mes, rec = make_mes(), Recorder()
    mes.attach(rec)
    mes.start_cell()
    mes.start_cell()
    mes.stop_cell()
    assert rec.types == [EventType.CELL_STARTED, EventType.CELL_STOPPED]


def test_failed_run_order_publishes_no_order_event():
    mes, rec = make_mes(), Recorder()
    mes.attach(rec)
    with pytest.raises(ValueError):
        mes.run_order("NO-EXISTE")
    assert EventType.ORDER_STARTED not in rec.types


def test_batch_event_carries_total_quantity():
    mes, rec = make_mes(), Recorder()
    mes.attach(rec, [EventType.ORDER_STARTED])
    mes.register_batch("LOTE", "L-1", [("B-1", "P", 20), ("B-2", "P", 30)])
    mes.process_order("LOTE")
    assert rec.events[0].data["quantity"] == 50


def test_detached_observer_stops_receiving_facade_events():
    mes, rec = make_mes(), Recorder()
    mes.attach(rec)
    mes.detach(rec)
    mes.register_order("O-3", "Pieza", 1)
    mes.process_order("O-3")
    assert rec.events == []


def test_metrics_observer_end_to_end_with_clock():
    clock = FakeClock(100.0)
    mes = make_mes(clock=clock)
    metrics = ProductionMetricsObserver()
    mes.attach(metrics)
    mes.register_order("O-4", "Pieza", 8)
    mes.process_order("O-4")
    clock.t = 160.0
    mes.stop_cell()
    assert metrics.operating_seconds() == 60.0
    assert metrics.quality_rate() == 1.0
    assert metrics.units_completed == 8


def test_commands_publish_events_through_the_facade():
    mes, rec = make_mes(), Recorder()
    mes.attach(rec)
    mes.register_order("O-5", "Pieza", 3)
    CommandInvoker().execute(ProcessOrderCommand(mes, "O-5"))
    assert EventType.ORDER_COMPLETED in rec.types


def test_denied_operation_publishes_no_events():
    service = ProductionServiceProxy(ProductionService(), "visita", "consulta")
    mes = ObservableMESFacade(
        CNCCellFactory(), production_service=service, logger=FakeLogger()
    )
    rec = Recorder()
    mes.attach(rec)
    with pytest.raises(PermissionError):
        mes.register_order("O-6", "Pieza", 1)
    assert rec.events == []
