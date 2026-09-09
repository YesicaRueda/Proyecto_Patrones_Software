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

seccion("CREACIÓN DE ÓRDENES (Builder + Factory Method)")
standard_creator = StandardOrderCreator()
urgent_creator = UrgentOrderCreator()

standard_data = OrderBuilder("OP-001", "Pieza metálica A", 100).build()
standard_order = standard_creator.create_order(standard_data)

urgent_data = (
    OrderBuilder("OP-002", "Pieza metálica B", 50)
    .with_lote("L-2026-09")
    .with_fecha_entrega(datetime(2026, 9, 20))
    .with_equipo_asignado("CNC-01")
    .build()
)
urgent_order = urgent_creator.create_order(urgent_data)

production.add_order(standard_order)
production.add_order(urgent_order)

print(f"{'Orden':<10}{'Producto':<20}{'Lote':<12}{'Entrega':<14}{'Equipo':<10}")
print(f"{standard_order.order_id:<10}{standard_order.product:<20}{'-':<12}{'-':<14}{'-':<10}")
print(f"{urgent_order.order_id:<10}{urgent_order.product:<20}"
      f"{urgent_order.lote:<12}{urgent_order.fecha_entrega.strftime('%Y-%m-%d'):<14}"
      f"{urgent_order.equipo_asignado:<10}")

seccion("COLA DE PRIORIDAD (antes de iniciar)")
for order in production.get_pending_queue():
    print(f"  {order.order_id:<8} prioridad={order.get_priority_score()}")

seccion("EJECUCIÓN DE ÓRDENES")
production.start_order("OP-001")
production.start_order_with_equipment("OP-002", equipment)

print(f"Estado OP-001: {production.get_order('OP-001').status}")
print(f"Estado OP-002: {production.get_order('OP-002').status}")

production.complete_order("OP-001")
print(f"Estado OP-001 (final): {production.get_order('OP-001').status}")