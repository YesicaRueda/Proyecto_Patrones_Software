from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
import copy

class ProductionOrder(ABC):

    def __init__(self, order_id, product, quantity, lote=None,
                 fecha_ingreso=None, fecha_entrega=None,
                 descripcion=None, equipo_asignado=None):
        self.order_id = order_id
        self.product = product
        self.quantity = quantity
        self.status = "Pendiente"
        self.lote = lote
        self.fecha_ingreso = fecha_ingreso
        self.fecha_entrega = fecha_entrega
        self.descripcion = descripcion
        self.equipo_asignado = equipo_asignado

    def start(self):
        self.status = "En producción"

    def complete(self):
        self.status = "Completada"

    @abstractmethod
    def get_priority_score(self) -> int:
        pass

    def clone(self, new_order_id, new_quantity=None):
        clone = copy.deepcopy(self)

        clone.order_id = new_order_id

        if new_quantity is not None:
            clone.quantity = new_quantity

        clone.status = "Pendiente"

        return clone

class StandardOrder(ProductionOrder):

    def __init__(self, order_id, product, quantity, lote=None,
                 fecha_ingreso=None, fecha_entrega=None,
                 descripcion=None, equipo_asignado=None):
        super().__init__(order_id, product, quantity, lote,
                          fecha_ingreso, fecha_entrega,
                          descripcion, equipo_asignado)
        self.priority = "Normal"

    def get_priority_score(self) -> int:
        return 1


class UrgentOrder(ProductionOrder):

    def __init__(self, order_id, product, quantity, lote=None,
                 fecha_ingreso=None, fecha_entrega=None,
                 descripcion=None, equipo_asignado=None):
        super().__init__(order_id, product, quantity, lote,
                          fecha_ingreso, fecha_entrega,
                          descripcion, equipo_asignado)
        self.priority = "Alta"

    def get_priority_score(self) -> int:
        return 10

