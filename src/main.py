from src.infrastructure.logger import Logger
from src.production.prod_service import ProductionService
from src.equipment.equipment_service import EquipmentService
from src.equipment.cell_factory import CNCCellFactory
from src.production.prod_factory import (
    StandardOrderCreator,
    UrgentOrderCreator
)
from datetime import datetime
from src.production.order_builder import OrderBuilder


def seccion(titulo):
    print(f"\n=== {titulo} ===")


seccion("SINGLETON - LOGGER")
logger1 = Logger.getInstance()
logger2 = Logger.getInstance()
print(f"Logger1 y Logger2 son la misma instancia: {logger1 is logger2}")

seccion("INICIALIZACIÓN DE SERVICIOS")
production = ProductionService()
equipment = EquipmentService(CNCCellFactory())
equipment.start_machine()

seccion("CREACIÓN DE ÓRDENES (Builder + Factory Method + Prototype)")

urgent_creator = UrgentOrderCreator()

plantilla_data = (
    OrderBuilder("OP-002", "Pieza metálica B", 50)
    .with_lote("L-2026-09")
    .with_fecha_entrega(datetime(2026, 9, 20))
    .with_equipo_asignado("CNC-01")
    .build()
)

plantilla = urgent_creator.create_order(plantilla_data)

urgent_order_2 = plantilla.clone("OP-003", 75)
urgent_order_3 = plantilla.clone("OP-004", 100)

production.add_order(plantilla)
production.add_order(urgent_order_2)
production.add_order(urgent_order_3)

print(f"{'Orden':<10}{'Producto':<20}{'Lote':<12}{'Entrega':<14}{'Equipo':<10}")
for order in production.get_pending_queue():
    print(f"{order.order_id:<10}{order.product:<20}"
          f"{order.lote:<12}{order.fecha_entrega.strftime('%Y-%m-%d'):<14}"
          f"{order.equipo_asignado:<10}")

seccion("COLA DE PRIORIDAD (antes de iniciar)")
for order in production.get_pending_queue():
    print(f"  {order.order_id:<8} prioridad={order.get_priority_score()}")

seccion("EJECUCIÓN DE ÓRDENES")
production.start_order_with_equipment("OP-002", equipment)

print(f"Estado OP-002: {production.get_order('OP-002').status}")
print(f"Estado OP-003: {production.get_order('OP-003').status}")
print(f"Estado OP-004: {production.get_order('OP-004').status}")