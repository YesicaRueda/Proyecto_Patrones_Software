

from src.infrastructure.logger import Logger

class ProductionService:     

    def __init__(self):
        self.orders = {}

    def add_order(self, order):
        if order.order_id in self.orders:
            raise ValueError(f"La orden {order.order_id} ya existe")

        self.orders[order.order_id] = order

        logger = Logger.getInstance()
        logger.log(f"Orden {order.order_id} registrada")

    def get_order(self, order_id):
        return self.orders.get(order_id)

    def start_order(self, order_id):
        order = self.get_order(order_id)

        if order is None:
            raise ValueError(f"Orden {order_id} no encontrada")

        if order.status != "Pendiente":
            raise ValueError(
                f"La orden {order_id} no se puede iniciar porque su estado es '{order.status}'"
            )

        order.start()

        logger = Logger.getInstance()
        logger.log(f"Orden de producción {order_id} iniciada")

    def complete_order(self, order_id):
        order = self.get_order(order_id)

        if order is None:
            raise ValueError(f"Orden {order_id} no encontrada")

        if order.status != "En producción":
            raise ValueError(
                f"La orden {order_id} no se puede completar porque su estado es '{order.status}'"
            )

        order.complete()

        logger = Logger.getInstance()
        logger.log(f"Orden de producción {order_id} completada")

    def get_pending_queue(self):
        pending = [
            order for order in self.orders.values()
            if order.status == "Pendiente"
        ]
        return sorted(
            pending,
            key=lambda order: order.get_priority_score(),
            reverse=True
        )
