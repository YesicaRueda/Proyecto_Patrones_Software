import pytest

from src.equipment.cell_factory import CNCCellFactory
from src.equipment.equipment_service import EquipmentService
from src.production.order_group import OrderGroup
from src.production.prod_order import StandardOrder, UrgentOrder
from src.production.prod_service import ProductionService


def make_group():
    group = OrderGroup("G-1", lote="L-1")
    group.add(StandardOrder("OP-1", "Pieza A", 10))
    group.add(UrgentOrder("OP-2", "Pieza B", 20))
    return group


def test_group_quantity_is_sum_of_children():
    group = make_group()
    assert group.quantity == 30


def test_group_priority_is_max_of_children():
    group = make_group()
    assert group.get_priority_score() == 10


def test_empty_group_has_zero_priority_and_is_pending():
    group = OrderGroup("G-0")
    assert group.get_priority_score() == 0
    assert group.quantity == 0
    assert group.status == "Pendiente"


def test_start_and_complete_propagate_to_children():
    group = make_group()

    group.start()
    assert all(child.status == "En producción" for child in group.children)
    assert group.status == "En producción"

    group.complete()
    assert all(child.status == "Completada" for child in group.children)
    assert group.status == "Completada"


def test_start_does_not_restart_children_already_completed():
    group = make_group()
    done = group.children[0]
    done.start()
    done.complete()

    group.start()

    assert done.status == "Completada"
    assert group.children[1].status == "En producción"


def test_group_status_is_in_production_when_children_differ():
    group = make_group()
    group.children[0].start()
    group.children[0].complete()

    assert group.status == "En producción"


def test_nested_groups_aggregate_recursively():
    inner = OrderGroup("G-IN")
    inner.add(StandardOrder("OP-3", "Pieza C", 5))

    outer = make_group()
    outer.add(inner)

    assert outer.quantity == 35
    assert outer.count_orders() == 3

    outer.start()
    assert inner.children[0].status == "En producción"


def test_group_cannot_contain_itself_or_its_ancestor():
    outer = OrderGroup("G-OUT")
    inner = OrderGroup("G-IN")
    outer.add(inner)

    with pytest.raises(ValueError):
        outer.add(outer)

    with pytest.raises(ValueError):
        inner.add(outer)


def test_group_rejects_duplicate_order_id():
    group = make_group()

    with pytest.raises(ValueError):
        group.add(StandardOrder("OP-1", "Otra pieza", 1))


def test_remove_child():
    group = make_group()
    first = group.children[0]

    group.remove(first)

    assert group.quantity == 20

    with pytest.raises(ValueError):
        group.remove(first)


def test_clone_group_is_independent_and_renames_children():
    group = make_group()
    group.start()

    copy = group.clone("G-2")

    assert copy.order_id == "G-2"
    assert [c.order_id for c in copy.children] == ["G-2-1", "G-2-2"]
    assert copy.quantity == group.quantity
    assert copy.status == "Pendiente"
    assert group.status == "En producción"

    copy.children[0].quantity = 999
    assert group.children[0].quantity == 10


def test_clone_group_rejects_new_quantity():
    group = make_group()

    with pytest.raises(ValueError):
        group.clone("G-2", 50)


def test_production_service_treats_group_as_a_single_order():
    service = ProductionService()
    equipment = EquipmentService(CNCCellFactory())
    equipment.start_machine()

    service.add_order(make_group())
    service.add_order(StandardOrder("OP-9", "Pieza Z", 1))

    queue = service.get_pending_queue()
    assert [o.order_id for o in queue] == ["G-1", "OP-9"]

    service.start_order_with_equipment("G-1", equipment)

    assert service.get_order("G-1").status == "En producción"
    assert all(c.status == "En producción" for c in service.get_order("G-1").children)

    service.complete_order("G-1")
    assert service.get_order("G-1").status == "Completada"
