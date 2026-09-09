from abc import ABC, abstractmethod
from src.production.prod_order import StandardOrder, UrgentOrder

class OrderCreator(ABC):

    @abstractmethod
    def create_order(self, order_id, product, quantity):
        pass


class StandardOrderCreator(OrderCreator):
    def create_order(self, order_data: dict):
        return StandardOrder(**order_data)


class UrgentOrderCreator(OrderCreator):
    def create_order(self, order_data: dict):
        return UrgentOrder(**order_data)