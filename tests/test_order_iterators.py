import pytest


from src.production.order_group import OrderGroup
from src.production.prod_order import StandardOrder, UrgentOrder
from src.production.order_iterators import (
    BreadthFirstIterator,
    DepthFirstIterator,
    OrderIterator,
    create_iterator,
    leaf_status_counts,
)


def ids(iterator):
    return [o.order_id for o in iterator]


@pytest.fixture
def lote():
    """G[A, SUB[B, C], D]"""
    g = OrderGroup("G", lote="L-1")
    sub = OrderGroup("SUB", lote="L-1")
    g.add(StandardOrder("A", "P", 1))
    sub.add(UrgentOrder("B", "P", 2))
    sub.add(StandardOrder("C", "P", 3))
    g.add(sub)
    g.add(StandardOrder("D", "P", 4))
    return g


def test_los_recorridos_son_iteradores(lote):
    assert isinstance(DepthFirstIterator(lote), OrderIterator)
    assert isinstance(BreadthFirstIterator(lote), OrderIterator)


def test_profundidad_devuelve_solo_hojas_en_orden(lote):
    assert ids(create_iterator(lote, "depth")) == ["A", "B", "C", "D"]


def test_amplitud_devuelve_hojas_por_niveles(lote):
    assert ids(create_iterator(lote, "breadth")) == ["A", "D", "B", "C"]


def test_profundidad_incluyendo_grupos(lote):
    result = ids(create_iterator(lote, "depth", leaves_only=False))
    assert result == ["G", "A", "SUB", "B", "C", "D"]


def test_amplitud_incluyendo_grupos(lote):
    result = ids(create_iterator(lote, "breadth", leaves_only=False))
    assert result == ["G", "A", "SUB", "D", "B", "C"]


def test_una_orden_individual_se_devuelve_a_si_misma():
    order = StandardOrder("X", "P", 1)
    assert ids(create_iterator(order)) == ["X"]


def test_grupo_vacio_no_devuelve_hojas():
    it = create_iterator(OrderGroup("VACIO"))
    assert it.has_next() is False
    assert list(it) == []


def test_anidamiento_profundo():
    g1, g2, g3 = OrderGroup("G1"), OrderGroup("G2"), OrderGroup("G3")
    g3.add(StandardOrder("Z", "P", 1))
    g2.add(g3)
    g1.add(g2)
    assert ids(create_iterator(g1)) == ["Z"]


def test_filtro_por_estado(lote):
    lote.children[1].start()  # inicia SUB
    assert ids(create_iterator(lote, status="En producción")) == ["B", "C"]
    assert ids(create_iterator(lote, status="Pendiente")) == ["A", "D"]


def test_protocolo_has_next_y_stop_iteration(lote):
    it = create_iterator(lote)
    seen = []
    while it.has_next():
        seen.append(next(it).order_id)
    assert seen == ["A", "B", "C", "D"]
    with pytest.raises(StopIteration):
        next(it)
    with pytest.raises(StopIteration):
        next(it)


def test_iteradores_independientes(lote):
    first, second = create_iterator(lote), create_iterator(lote)
    assert next(first).order_id == "A"
    assert next(first).order_id == "B"
    assert next(second).order_id == "A"


def test_recorrer_no_modifica_el_grupo(lote):
    before = (lote.quantity, lote.status, [c.order_id for c in lote.children])
    list(create_iterator(lote))
    assert (lote.quantity, lote.status, [c.order_id for c in lote.children]) == before


def test_conteo_de_hojas_por_estado(lote):
    suelta = StandardOrder("S", "P", 1)
    lote.children[1].start()
    assert leaf_status_counts([lote, suelta]) == {"Pendiente": 3, "En producción": 2}


def test_estrategia_desconocida(lote):
    with pytest.raises(ValueError):
        create_iterator(lote, "aleatoria")
