
from src.infrastructure.logger import Logger
from src.equipment.cell_factory import AbstractProductionCellFactory


class EquipmentService:

    def __init__(self, factory: AbstractProductionCellFactory):
        self.factory = factory
        self.equipment = factory.create_equipment()
        self.inspection = factory.create_inspection()

    def start_machine(self):
        self.equipment.start()
        logger = Logger.getInstance()
        logger.log(f"{type(self.equipment).__name__} en operación")

    def stop_machine(self):
        self.equipment.stop()
        logger = Logger.getInstance()
        logger.log(f"{type(self.equipment).__name__} detenida")

    def run_inspection(self, order):
        result = self.inspection.inspect(order)
        logger = Logger.getInstance()
        logger.log(f"Inspección de {type(self.equipment).__name__}: {result}")
        return result