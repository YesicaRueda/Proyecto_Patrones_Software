

from infrastructure.logger import Logger

class ProductionService:

    #  -antes que era el main quien creaba la orden
    # def start_order(self, order): 
    #     logger = Logger.getInstance()

    #     order.start()

    #     logger.log(
    #         f"Orden de producción {order.order_id} iniciada"
    #     )        

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

    