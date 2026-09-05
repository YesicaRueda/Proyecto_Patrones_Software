
from src.production.prod_order import StandardOrder, UrgentOrder
from src.production.prod_service import ProductionService

def test_urgent_order_has_higher_score_than_standard():
    standard = StandardOrder("1", "tornillo", 10)
    urgent = UrgentOrder("2", "tornillo", 10)

    assert urgent.get_priority_score() > standard.get_priority_score()

def test_pending_queue_orders_urgent_first():
    service = ProductionService()
    service.add_order(StandardOrder("1", "tornillo", 10))
    service.add_order(UrgentOrder("2", "tuerca", 5))
    service.add_order(StandardOrder("3", "tornillo", 20))

    queue = service.get_pending_queue()

    assert queue[0].order_id == "2"          # la urgente va primero
    assert [o.order_id for o in queue] == ["2", "1", "3"]

def test_pending_queue_excludes_started_orders():
    service = ProductionService()
    service.add_order(UrgentOrder("1", "tornillo", 10))
    service.start_order("1")

    assert service.get_pending_queue() == []