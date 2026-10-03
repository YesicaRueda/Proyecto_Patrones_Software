import time

from src.equipment.equipment_base import Inspection
from src.infrastructure.logger import Logger


class InspectionDecorator(Inspection):
    """Decorator base: envuelve una Inspection y delega en ella.

    Implementa la misma interfaz (`inspect`), por lo que EquipmentService
    no distingue entre una inspección simple y una decorada.
    """

    def __init__(self, wrapped: Inspection):
        self._wrapped = wrapped

    def inspect(self, order) -> bool:
        return self._wrapped.inspect(order)


class LoggedInspection(InspectionDecorator):
    """Registra en el Logger el inicio y el resultado de cada inspección."""

    def __init__(self, wrapped: Inspection, logger=None):
        super().__init__(wrapped)
        self._logger = logger

    def inspect(self, order) -> bool:
        logger = self._logger or Logger.getInstance()

        logger.log(f"Inspección iniciada para la orden {order.order_id}")
        result = super().inspect(order)

        if result:
            logger.log(f"Inspección aprobada para la orden {order.order_id}")
        else:
            logger.log(
                f"Inspección rechazada para la orden {order.order_id}",
                "WARNING",
            )

        return result


class TimedInspection(InspectionDecorator):
    """Mide cuánto tarda cada inspección (disponible en `last_duration`)."""

    def __init__(self, wrapped: Inspection, clock=time.perf_counter):
        super().__init__(wrapped)
        self._clock = clock
        self.last_duration = None

    def inspect(self, order) -> bool:
        start = self._clock()
        try:
            return super().inspect(order)
        finally:
            self.last_duration = self._clock() - start
