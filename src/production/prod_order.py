

class ProductionOrder:

    def __init__(self, order_id, product, quantity):
        self.order_id = order_id
        self.product = product
        self.quantity = quantity
        self.status = "Pendiente"

    def start(self):
        self.status = "En producción"

    def complete(self):
        self.status = "Completada"

    def get_priority_score(self) -> int: raise NotImplementedError("Cada tipo de orden debe definir su propio score")

class StandardOrder(ProductionOrder):

    def __init__(self, order_id, product, quantity):
        super().__init__(order_id, product, quantity)
        self.priority = "Normal"

    def get_priority_score(self) -> int:
        return 1


class UrgentOrder(ProductionOrder):

    def __init__(self, order_id, product, quantity):
        super().__init__(order_id, product, quantity)
        self.priority = "Alta"

    def get_priority_score(self) -> int:
        return 10

