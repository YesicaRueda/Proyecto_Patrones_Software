
from abc import ABC, abstractmethod
from collections import deque

from src.production.order_group import OrderGroup

_END = object()


class OrderIterator(ABC):
    """Iterator: interfaz común de los recorridos de órdenes."""

    def __iter__(self):
        return self

    @abstractmethod
    def has_next(self) -> bool:
        """Indica si quedan órdenes por recorrer."""

    @abstractmethod
    def __next__(self):
        """Devuelve la siguiente orden o lanza StopIteration."""


class _TraversalIterator(OrderIterator):
    """Base de los recorridos: define el esqueleto y delega el orden."""

    def __init__(self, root, leaves_only=True, status=None):
        self._leaves_only = leaves_only
        self._status = status
        self._frontier = deque([root])
        self._lookahead = self._advance()

    @abstractmethod
    def _pop(self):
        """Extrae el siguiente nodo de la frontera."""

    @abstractmethod
    def _expand(self, group):
        """Agrega a la frontera los hijos de un grupo."""

    def _advance(self):
        while self._frontier:
            node = self._pop()
            if isinstance(node, OrderGroup):
                self._expand(node)
                if self._leaves_only:
                    continue
            if self._status is not None and node.status != self._status:
                continue
            return node
        return _END

    def has_next(self) -> bool:
        return self._lookahead is not _END

    def __next__(self):
        if self._lookahead is _END:
            raise StopIteration
        current = self._lookahead
        self._lookahead = self._advance()
        return current


class DepthFirstIterator(_TraversalIterator):
    """Recorrido en profundidad (preorden): termina un subgrupo antes de seguir."""

    def _pop(self):
        return self._frontier.pop()

    def _expand(self, group):
        self._frontier.extend(reversed(group.children))


class BreadthFirstIterator(_TraversalIterator):
    """Recorrido por niveles: primero los hijos directos, luego los nietos."""

    def _pop(self):
        return self._frontier.popleft()

    def _expand(self, group):
        self._frontier.extend(group.children)


_STRATEGIES = {"depth": DepthFirstIterator, "breadth": BreadthFirstIterator}


def create_iterator(root, strategy="depth", leaves_only=True, status=None):
    """Crea el iterador pedido para una orden o un grupo de órdenes."""
    try:
        iterator_class = _STRATEGIES[strategy]
    except KeyError:
        raise ValueError(
            f"Estrategia de recorrido desconocida: '{strategy}'. "
            f"Use: {', '.join(_STRATEGIES)}"
        ) from None
    return iterator_class(root, leaves_only=leaves_only, status=status)


def leaf_status_counts(orders):
    """Cuenta las órdenes individuales por estado, abriendo los lotes."""
    counts = {}
    for root in orders:
        for leaf in DepthFirstIterator(root, leaves_only=True):
            counts[leaf.status] = counts.get(leaf.status, 0) + 1
    return counts
