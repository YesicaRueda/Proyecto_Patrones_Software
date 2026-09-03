

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

class StandardOrder(ProductionOrder):

    def __init__(self, order_id, product, quantity):
        super().__init__(order_id, product, quantity)
        self.priority = "Normal"


class UrgentOrder(ProductionOrder):

    def __init__(self, order_id, product, quantity):
        super().__init__(order_id, product, quantity)
        self.priority = "Alta"