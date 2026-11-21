"""Patrón Strategy: políticas de planificación de la cola de producción.

`ProductionService.get_pending_queue()` ordena siempre por prioridad. Aquí se
encapsula cada regla de ordenamiento en una estrategia intercambiable y un
planificador (el contexto) que la aplica sobre las órdenes pendientes, sin
modificar `ProductionService` ni las órdenes.
"""
from abc import ABC, abstractmethod

from src.infrastructure.logger import Logger

PENDING = "Pendiente"


class SchedulingStrategy(ABC):
    """Regla para decidir en qué orden se atienden las órdenes pendientes."""

    key = ""          # identificador estable (para selectores y pruebas)
    label = ""        # nombre legible
    description = ""  # una línea que explica el criterio

    @abstractmethod
    def order(self, orders):
        """Devuelve una lista nueva con las órdenes en el orden de atención.

        `orders` llega en orden de registro. Las estrategias no deben
        modificar las órdenes ni la lista recibida.
        """


class PriorityStrategy(SchedulingStrategy):
    """Mayor prioridad primero (la regla que ya usa `get_pending_queue()`)."""

    key = "priority"
    label = "Prioridad"
    description = "Urgentes primero; a igual prioridad, por orden de registro"

    def order(self, orders):
        return sorted(orders, key=lambda o: o.get_priority_score(), reverse=True)


class FifoStrategy(SchedulingStrategy):
    """Primero en llegar, primero en atenderse."""

    key = "fifo"
    label = "Orden de llegada"
    description = "Se atiende según el orden en que se registraron"

    def order(self, orders):
        return list(orders)


class DueDateStrategy(SchedulingStrategy):
    """Fecha de entrega más cercana primero; sin fecha, al final."""

    key = "due_date"
    label = "Fecha de entrega"
    description = "La entrega más próxima primero; sin fecha, al final"

    def order(self, orders):
        def key(order):
            due = getattr(order, "fecha_entrega", None)
            return (due is None, due)

        return sorted(orders, key=key)


class SmallestFirstStrategy(SchedulingStrategy):
    """Menor cantidad primero: libera pedidos pequeños con rapidez."""

    key = "smallest"
    label = "Menor cantidad"
    description = "Las órdenes más pequeñas primero"

    def order(self, orders):
        return sorted(orders, key=lambda o: o.quantity)


STRATEGIES = {
    strategy.key: strategy
    for strategy in (PriorityStrategy(), FifoStrategy(),
                     DueDateStrategy(), SmallestFirstStrategy())
}


def get_strategy(key):
    """Devuelve la estrategia registrada con esa clave."""
    try:
        return STRATEGIES[key]
    except KeyError:
        raise ValueError(f"Política de planificación desconocida: {key}") from None


class ProductionScheduler:
    """Contexto: aplica la estrategia vigente sobre las órdenes pendientes."""

    def __init__(self, strategy=None, logger=None):
        self._logger = logger
        self._strategy = PriorityStrategy()
        if strategy is not None:
            self._set(strategy)

    @property
    def strategy(self):
        return self._strategy

    def set_strategy(self, strategy):
        """Cambia la política en tiempo de ejecución y lo deja en el Logger."""
        self._set(strategy)
        self._log(f"Política de planificación: {type(strategy).__name__} "
                  f"({strategy.label})")

    def queue(self, production):
        """Órdenes pendientes de `production`, en el orden de la política."""
        pending = [o for o in production.orders.values() if o.status == PENDING]
        return self._strategy.order(pending)

    def next_order(self, production):
        """La orden que corresponde atender ahora (None si no hay pendientes)."""
        queue = self.queue(production)
        return queue[0] if queue else None

    def _set(self, strategy):
        if not isinstance(strategy, SchedulingStrategy):
            raise TypeError("La política debe implementar SchedulingStrategy")
        self._strategy = strategy

    def _log(self, message, level="INFO"):
        logger = self._logger or Logger.getInstance()
        logger.log(message, level)
