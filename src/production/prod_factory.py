

from abc import ABC, abstractmethod
from production.prod_order import StandardOrder, UrgentOrder

class OrderCreator(ABC):

    @abstractmethod
    def create_order(self, order_id, product, quantity):
        pass


class StandardOrderCreator(OrderCreator):

    def create_order(self, order_id, product, quantity):
        return StandardOrder(order_id, product, quantity)


class UrgentOrderCreator(OrderCreator):

    def create_order(self, order_id, product, quantity):
        return UrgentOrder(order_id, product, quantity)