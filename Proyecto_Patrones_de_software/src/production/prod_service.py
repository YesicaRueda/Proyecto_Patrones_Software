from infrastructure.logger import Logger


class ProductionService:

    def start_order(self, order_id):
        logger = Logger.getInstance()
        logger.log(f"Orden de producción {order_id} iniciada")