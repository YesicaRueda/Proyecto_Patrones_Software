"""MESFacade que publica eventos a sus observadores (patrón Observer).

Es una subclase: `MESFacade` no se modifica. Toda operación que pase por
la fachada (directa o mediante Command) publica sus eventos.
"""
import time
from types import MappingProxyType

from src.facade.mes_facade import MESFacade
from src.observer.observer import EventType, MESEvent, Subject


class ObservableMESFacade(MESFacade, Subject):
    def __init__(self, *args, clock=None, logger=None, **kwargs):
        MESFacade.__init__(self, *args, **kwargs)
        Subject.__init__(self, logger=logger)
        self._clock = clock or time.monotonic
        self._cell_published = self._cell_operating()

    # --- utilidades internas -------------------------------------------
    def cell_status(self):
        """Estado del equipo ("Parada" u "Operando").

        `EquipmentService` no expone `status`: el estado vive en la máquina
        (`equipment.equipment.status`). Se lee primero del servicio, por si
        algún día lo expone, y si no existe se lee de la máquina.
        """
        service = self.equipment
        status = getattr(service, "status", None)
        if status is None:
            status = getattr(getattr(service, "equipment", None), "status", None)
        return status

    def _cell_operating(self):
        return self.cell_status() == "Operando"

    def _publish(self, event_type, order_id=None, **data):
        self.notify(
            MESEvent(event_type, self._clock(), order_id,
                     MappingProxyType(dict(data)))
        )

    def _sync_cell(self):
        """Publica un evento de equipo solo cuando su estado realmente cambió.

        Comparar contra el último estado publicado evita duplicados sin
        importar si `run_order` arranca el equipo por `start_cell` o no.
        """
        operating = self._cell_operating()
        if operating != self._cell_published:
            self._cell_published = operating
            self._publish(
                EventType.CELL_STARTED if operating else EventType.CELL_STOPPED
            )

    # --- operaciones observadas ----------------------------------------
    def start_cell(self):
        try:
            return super().start_cell()
        finally:
            self._sync_cell()

    def stop_cell(self):
        try:
            return super().stop_cell()
        finally:
            self._sync_cell()

    def run_order(self, order_id):
        try:
            result = super().run_order(order_id)
        finally:
            self._sync_cell()
        order = self.production.get_order(order_id)
        self._publish(
            EventType.ORDER_STARTED,
            order_id,
            quantity=getattr(order, "quantity", None),
            priority=order.get_priority_score() if order is not None else None,
        )
        return result

    def finish_order(self, order_id):
        order = self.production.get_order(order_id)
        quantity = getattr(order, "quantity", None)
        approved = super().finish_order(order_id)
        if approved:
            self._publish(EventType.INSPECTION_APPROVED, order_id, quantity=quantity)
            self._publish(EventType.ORDER_COMPLETED, order_id, quantity=quantity)
        else:
            self._publish(EventType.INSPECTION_REJECTED, order_id, quantity=quantity)
        return approved

    def process_order(self, order_id):
        # Misma definición que MESFacade: run_order + finish_order.
        self.run_order(order_id)
        return self.finish_order(order_id)
