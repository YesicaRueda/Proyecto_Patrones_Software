

from src.equipment.production_unit import ProductionUnit


class ProductionLine(ProductionUnit):

    def __init__(self, name: str):
        self.name = name
        self._units = []

    def add_unit(self, unit: ProductionUnit):
        self._units.append(unit)

    def start(self):
        for unit in self._units:
            unit.start()

    def stop(self):
        for unit in self._units:
            unit.stop()

    def status(self):
        return [unit.status() for unit in self._units]