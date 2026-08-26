from infrastructure.logger import Logger
from production.prod_service import ProductionService
from equipment.equi_service import EquipmentService


logger1 = Logger.getInstance()
logger2 = Logger.getInstance()

print("¿Logger 1 y Logger 2 son la misma instancia?", logger1 is logger2)

production = ProductionService()
equipment = EquipmentService()

production.start_order("OP-001")
equipment.start_machine("CNC-01")