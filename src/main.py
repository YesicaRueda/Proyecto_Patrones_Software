

from src.infrastructure.logger import Logger
from src.production.prod_service import ProductionService
from src.equipment.equi_service import EquipmentService
from src.production.prod_factory import (
    StandardOrderCreator,
    UrgentOrderCreator
)


logger1 = Logger.getInstance()
logger2 = Logger.getInstance()

print("¿Logger 1 y Logger 2 son la misma instancia?", logger1 is logger2)

production = ProductionService()
equipment = EquipmentService()

standard_creator = StandardOrderCreator()
urgent_creator = UrgentOrderCreator()

standard_order = standard_creator.create_order(
    "OP-001",
    "Pieza metálica A",
    100
)

urgent_order = urgent_creator.create_order(
    "OP-002",
    "Pieza metálica B",
    50
)

production.add_order(standard_order)
production.add_order(urgent_order)

production.start_order("OP-001")
production.start_order("OP-002")

print(
    "Estado OP-001:",
    production.get_order("OP-001").status
)

print(
    "Estado OP-002:",
    production.get_order("OP-002").status
)

production.complete_order("OP-001")

print(
    "Estado OP-001:",
    production.get_order("OP-001").status
)


equipment.start_machine("CNC-01")