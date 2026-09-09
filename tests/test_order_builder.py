from datetime import datetime
from src.production.order_builder import OrderBuilder
from src.production.prod_factory import StandardOrderCreator, UrgentOrderCreator
from src.production.prod_order import StandardOrder, UrgentOrder


def test_builder_produces_dict_with_required_fields():
    data = OrderBuilder("OP-100", "Pieza A", 10).build()

    assert data["order_id"] == "OP-100"
    assert data["lote"] is None
    assert data["fecha_entrega"] is None


def test_creator_uses_builder_data_for_urgent_order():
    entrega = datetime(2026, 9, 20)
    data = (
        OrderBuilder("OP-101", "Pieza B", 5)
        .with_lote("L-01")
        .with_fecha_entrega(entrega)
        .with_descripcion("Pieza urgente para cliente X")
        .with_equipo_asignado("CNC-01")
        .build()
    )

    order = UrgentOrderCreator().create_order(data)

    assert isinstance(order, UrgentOrder)
    assert order.lote == "L-01"
    assert order.fecha_entrega == entrega
    assert order.get_priority_score() == 10


def test_creator_uses_builder_data_for_standard_order():
    data = OrderBuilder("OP-102", "Pieza C", 20).build()
    order = StandardOrderCreator().create_order(data)

    assert isinstance(order, StandardOrder)
    assert order.get_priority_score() == 1