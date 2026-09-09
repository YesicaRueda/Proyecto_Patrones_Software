from src.production.prod_order import UrgentOrder


def test_clone_order():
    original = UrgentOrder(
        order_id="OP-001",
        product="Producto A",
        quantity=100,
        lote="LOTE-01",
        fecha_entrega="2026-09-15",
        equipo_asignado="CNC-01"
    )

    original.status = "Completada"

    clone = original.clone("OP-002", 50)

    assert clone is not original
    assert clone.lote == original.lote
    assert clone.fecha_entrega == original.fecha_entrega
    assert clone.equipo_asignado == original.equipo_asignado
    assert clone.order_id == "OP-002"
    assert clone.quantity == 50
    assert clone.status == "Pendiente"