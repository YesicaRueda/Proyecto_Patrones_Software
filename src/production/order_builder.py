from datetime import datetime
from src.production.prod_order import StandardOrder, UrgentOrder


class OrderBuilder:

    def __init__(self, order_id, product, quantity):
        self._order_id = order_id
        self._product = product
        self._quantity = quantity
        self._lote = None
        self._fecha_ingreso = None
        self._fecha_entrega = None
        self._descripcion = None
        self._equipo_asignado = None

    def with_lote(self, lote: str):
        self._lote = lote
        return self

    def with_fecha_ingreso(self, fecha: datetime):
        self._fecha_ingreso = fecha
        return self

    def with_fecha_entrega(self, fecha: datetime):
        self._fecha_entrega = fecha
        return self

    def with_descripcion(self, descripcion: str):
        self._descripcion = descripcion
        return self

    def with_equipo_asignado(self, equipo: str):
        self._equipo_asignado = equipo
        return self

    def build(self) -> dict:
        return {
            "order_id": self._order_id,
            "product": self._product,
            "quantity": self._quantity,
            "lote": self._lote,
            "fecha_ingreso": self._fecha_ingreso,
            "fecha_entrega": self._fecha_entrega,
            "descripcion": self._descripcion,
            "equipo_asignado": self._equipo_asignado,
        }