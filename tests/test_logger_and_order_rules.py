import pytest

from src.infrastructure.logger import Logger
from src.production.prod_order import ProductionOrder, StandardOrder
from src.production.prod_service import ProductionService


def test_production_order_cannot_be_instantiated():
    with pytest.raises(TypeError):
        ProductionOrder("1", "tornillo", 10)


def test_logger_getinstance_and_constructor_are_the_same_instance():
    logger1 = Logger.getInstance()
    logger2 = Logger.getInstance()
    logger3 = Logger()

    assert logger1 is logger2
    assert logger2 is logger3


def test_add_order_rejects_duplicate_order_id():
    service = ProductionService()
    service.add_order(StandardOrder("1", "tornillo", 10))

    with pytest.raises(ValueError):
        service.add_order(StandardOrder("1", "tuerca", 5))


def test_start_order_rejects_already_started_order():
    service = ProductionService()
    service.add_order(StandardOrder("1", "tornillo", 10))
    service.start_order("1")

    with pytest.raises(ValueError):
        service.start_order("1")


def test_start_order_rejects_completed_order():
    service = ProductionService()
    service.add_order(StandardOrder("1", "tornillo", 10))
    service.start_order("1")
    service.complete_order("1")

    with pytest.raises(ValueError):
        service.start_order("1")


def test_complete_order_rejects_order_that_never_started():
    service = ProductionService()
    service.add_order(StandardOrder("1", "tornillo", 10))

    with pytest.raises(ValueError):
        service.complete_order("1")
