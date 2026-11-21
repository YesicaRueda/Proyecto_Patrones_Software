from datetime import datetime
from types import SimpleNamespace

import pytest

from src.production.order_builder import OrderBuilder
from src.production.prod_factory import StandardOrderCreator, UrgentOrderCreator
from src.production.prod_order import StandardOrder
from src.production.prod_service import ProductionService
from src.strategy.scheduling import (
    STRATEGIES,
    DueDateStrategy,
    FifoStrategy,
    PriorityStrategy,
    ProductionScheduler,
    SchedulingStrategy,
    SmallestFirstStrategy,
    get_strategy,
)


class FakeLogger:
    def __init__(self):
        self.records = []

    def log(self, message, level="INFO"):
        self.records.append((level, message))


def fake(order_id, priority=1, quantity=10, due=None, status="Pendiente"):
    """Orden mínima: solo lo que las estrategias leen."""
    return SimpleNamespace(order_id=order_id, quantity=quantity, fecha_entrega=due,
                           status=status, get_priority_score=lambda: priority)


def ids(orders):
    return [o.order_id for o in orders]


def real_order(creator, order_id, quantity, due=None):
    builder = OrderBuilder(order_id, "Pieza", quantity)
    if due is not None:
        builder = builder.with_fecha_entrega(due)
    return creator.create_order(builder.build())


@pytest.fixture
def plant():
    """Cuatro órdenes reales con criterios que dan un orden distinto en cada política."""
    service = ProductionService()
    service.add_order(real_order(StandardOrderCreator(), "S-1", 40, datetime(2026, 12, 20)))
    service.add_order(real_order(UrgentOrderCreator(), "S-2", 25, datetime(2026, 12, 28)))
    service.add_order(real_order(StandardOrderCreator(), "S-3", 10, datetime(2026, 12, 15)))
    service.add_order(real_order(UrgentOrderCreator(), "S-4", 60, datetime(2026, 12, 18)))
    return service


# ------------------------------------------------------ estrategias (puras)
def test_priority_puts_highest_first_and_keeps_registration_order_on_ties():
    orders = [fake("A", 1), fake("B", 5), fake("C", 1), fake("D", 5)]
    assert ids(PriorityStrategy().order(orders)) == ["B", "D", "A", "C"]


def test_fifo_keeps_registration_order():
    orders = [fake("A", 9), fake("B", 1), fake("C", 5)]
    assert ids(FifoStrategy().order(orders)) == ["A", "B", "C"]


def test_due_date_sorts_ascending_and_orders_without_date_go_last():
    orders = [fake("A", due=datetime(2026, 12, 20)), fake("B"),
              fake("C", due=datetime(2026, 12, 1)), fake("D")]
    assert ids(DueDateStrategy().order(orders)) == ["C", "A", "B", "D"]


def test_smallest_first_sorts_by_quantity():
    orders = [fake("A", quantity=30), fake("B", quantity=5), fake("C", quantity=12)]
    assert ids(SmallestFirstStrategy().order(orders)) == ["B", "C", "A"]


def test_strategies_return_a_new_list_without_touching_the_input():
    orders = [fake("A", 1), fake("B", 5)]
    for strategy in STRATEGIES.values():
        result = strategy.order(orders)
        assert result is not orders
        assert ids(orders) == ["A", "B"]


def test_registry_exposes_every_strategy_with_label_and_description():
    assert set(STRATEGIES) == {"priority", "fifo", "due_date", "smallest"}
    for key, strategy in STRATEGIES.items():
        assert strategy.key == key and strategy.label and strategy.description
        assert isinstance(strategy, SchedulingStrategy)


def test_get_strategy_rejects_unknown_key():
    assert isinstance(get_strategy("fifo"), FifoStrategy)
    with pytest.raises(ValueError):
        get_strategy("no-existe")


def test_abstract_strategy_cannot_be_instantiated():
    with pytest.raises(TypeError):
        SchedulingStrategy()


# ----------------------------------------------- planificador (con fakes)
class FakeProduction:
    def __init__(self, *orders):
        self.orders = {o.order_id: o for o in orders}


def test_scheduler_defaults_to_priority_and_only_considers_pending_orders():
    production = FakeProduction(fake("A", 1), fake("B", 9, status="En producción"),
                                fake("C", 5), fake("D", 9, status="Completada"))
    scheduler = ProductionScheduler()
    assert isinstance(scheduler.strategy, PriorityStrategy)
    assert ids(scheduler.queue(production)) == ["C", "A"]


def test_scheduler_switches_strategy_at_runtime_and_logs_it():
    logger = FakeLogger()
    production = FakeProduction(fake("A", 1, quantity=30), fake("B", 5, quantity=5))
    scheduler = ProductionScheduler(logger=logger)
    assert scheduler.next_order(production).order_id == "B"
    scheduler.set_strategy(FifoStrategy())
    assert scheduler.next_order(production).order_id == "A"
    assert logger.records == [("INFO", "Política de planificación: FifoStrategy (Orden de llegada)")]


def test_scheduler_rejects_objects_that_are_not_strategies():
    with pytest.raises(TypeError):
        ProductionScheduler().set_strategy(object())
    with pytest.raises(TypeError):
        ProductionScheduler(strategy="fifo")


def test_next_order_is_none_when_nothing_is_pending():
    assert ProductionScheduler().next_order(FakeProduction()) is None


# ------------------------------------------- integración con el proyecto real
def test_priority_strategy_matches_get_pending_queue(plant):
    scheduler = ProductionScheduler(PriorityStrategy())
    planned = [o.get_priority_score() for o in scheduler.queue(plant)]
    existing = [o.get_priority_score() for o in plant.get_pending_queue()]
    assert planned == existing


@pytest.mark.parametrize("key, expected", [
    ("priority", ["S-2", "S-4", "S-1", "S-3"]),
    ("fifo", ["S-1", "S-2", "S-3", "S-4"]),
    ("due_date", ["S-3", "S-4", "S-1", "S-2"]),
    ("smallest", ["S-3", "S-2", "S-1", "S-4"]),
])
def test_each_policy_orders_real_orders_differently(plant, key, expected):
    scheduler = ProductionScheduler(get_strategy(key))
    assert ids(scheduler.queue(plant)) == expected


def test_scheduler_does_not_change_production_service(plant):
    before = {i: o.status for i, o in plant.orders.items()}
    scheduler = ProductionScheduler(DueDateStrategy())
    scheduler.queue(plant)
    assert {i: o.status for i, o in plant.orders.items()} == before


def test_started_orders_leave_the_planned_queue(plant):
    plant.start_order("S-3")
    assert "S-3" not in ids(ProductionScheduler(DueDateStrategy()).queue(plant))


def test_orders_without_due_date_work_with_real_orders():
    service = ProductionService()
    service.add_order(StandardOrder("N-1", "Pieza", 5))
    service.add_order(real_order(StandardOrderCreator(), "N-2", 5, datetime(2026, 12, 1)))
    assert ids(ProductionScheduler(DueDateStrategy()).queue(service)) == ["N-2", "N-1"]
