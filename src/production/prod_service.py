
from src.production.prod_order import StandardOrder, UrgentOrder
from src.infrastructure.logger import Logger

class ProductionService:     

    def __init__(self):
        self.orders = {}

    def add_order(self, order):
        self.orders[order.order_id] = order

        logger = Logger.getInstance()
        logger.log(f"Orden {order.order_id} registrada")

    def get_order(self, order_id):
        return self.orders.get(order_id)

    def start_order(self, order_id):
        order = self.get_order(order_id)

        if order is None:
            raise ValueError(f"Orden {order_id} no encontrada")

        order.start()

        logger = Logger.getInstance()
        logger.log(f"Orden de producción {order_id} iniciada")

    def complete_order(self, order_id):
        order = self.get_order(order_id)

        if order is None:
            raise ValueError(f"Orden {order_id} no encontrada")

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
