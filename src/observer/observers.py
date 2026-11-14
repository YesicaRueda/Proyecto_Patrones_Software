"""Observadores concretos del MES."""
from src.infrastructure.logger import Logger
from src.observer.observer import EventType, MESEvent, Observer


class ProductionMetricsObserver(Observer):
    """Acumula contadores y tiempos a partir de los eventos de planta.

    Es la base de datos que necesitará el cálculo de OEE: tiempo operativo
    (disponibilidad) y unidades aprobadas frente a inspeccionadas (calidad).
    El rendimiento requiere un tiempo de ciclo ideal que el dominio aún no
    define, por lo que no se calcula aquí.
    """

    def __init__(self):
        self.orders_started = 0
        self.orders_completed = 0
        self.units_completed = 0
        self.inspections_approved = 0
        self.inspections_rejected = 0
        self.units_approved = 0
        self.units_inspected = 0
        self.cell_starts = 0
        self._operating_seconds = 0.0
        self._operating_since = None
        self._first_timestamp = None

    def update(self, event: MESEvent) -> None:
        if self._first_timestamp is None:
            self._first_timestamp = event.timestamp
        quantity = event.data.get("quantity", 0) or 0

        if event.type == EventType.CELL_STARTED:
            if self._operating_since is None:
                self._operating_since = event.timestamp
                self.cell_starts += 1
        elif event.type == EventType.CELL_STOPPED:
            if self._operating_since is not None:
                self._operating_seconds += event.timestamp - self._operating_since
                self._operating_since = None
        elif event.type == EventType.ORDER_STARTED:
            self.orders_started += 1
        elif event.type == EventType.ORDER_COMPLETED:
            self.orders_completed += 1
            self.units_completed += quantity
        elif event.type == EventType.INSPECTION_APPROVED:
            self.inspections_approved += 1
            self.units_approved += quantity
            self.units_inspected += quantity
        elif event.type == EventType.INSPECTION_REJECTED:
            self.inspections_rejected += 1
            self.units_inspected += quantity

    def quality_rate(self):
        """Unidades aprobadas / unidades inspeccionadas (None si no hay datos)."""
        if self.units_inspected == 0:
            return None
        return self.units_approved / self.units_inspected

    def operating_seconds(self, now=None):
        """Tiempo operativo; con `now` incluye el intervalo aún abierto."""
        total = self._operating_seconds
        if self._operating_since is not None and now is not None:
            total += max(0.0, now - self._operating_since)
        return total

    def availability(self, now):
        """Tiempo operativo / tiempo observado (None si no hay ventana)."""
        if self._first_timestamp is None or now <= self._first_timestamp:
            return None
        observed = now - self._first_timestamp
        return min(1.0, self.operating_seconds(now) / observed)

    def snapshot(self, now=None):
        return {
            "orders_started": self.orders_started,
            "orders_completed": self.orders_completed,
            "units_completed": self.units_completed,
            "inspections_approved": self.inspections_approved,
            "inspections_rejected": self.inspections_rejected,
            "quality_rate": self.quality_rate(),
            "operating_seconds": self.operating_seconds(now),
        }


class RejectionAlertObserver(Observer):
    """Registra una alerta por cada inspección rechazada."""

    def __init__(self, logger=None):
        self._logger = logger
        self._alerts = []

    @property
    def alerts(self):
        return tuple(self._alerts)

    def update(self, event: MESEvent) -> None:
        if event.type != EventType.INSPECTION_REJECTED:
            return
        self._alerts.append((event.order_id, event.timestamp))
        logger = self._logger or Logger.getInstance()
        logger.log(
            f"ALERTA: inspección rechazada para la orden {event.order_id}",
            "WARNING",
        )
