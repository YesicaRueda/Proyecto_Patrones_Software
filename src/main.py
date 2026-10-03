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
from src.production.order_group import OrderGroup
from src.production.prod_order import StandardOrder
from src.equipment.inspection_decorators import (
    LoggedInspection,
    TimedInspection
)


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

seccion("COMPOSITE - LOTE DE ÓRDENES")
lote = OrderGroup("LOTE-01", lote="L-2026-09")
lote.add(plantilla.clone("OP-010", 20))
lote.add(plantilla.clone("OP-011", 30))

subgrupo = OrderGroup("LOTE-01-B", lote="L-2026-09")
subgrupo.add(StandardOrder("OP-012", "Pieza metálica C", 15))
lote.add(subgrupo)

production.add_order(lote)

print(f"Órdenes individuales en el lote: {lote.count_orders()}")
print(f"Cantidad total del lote: {lote.quantity}")
print(f"Prioridad del lote (máxima de sus hijos): {lote.get_priority_score()}")
print(f"Estado del lote: {lote.status}")

production.start_order_with_equipment("LOTE-01", equipment)

print(f"Estado del lote tras iniciarlo: {lote.status}")
for hijo in lote.children:
    print(f"  {hijo.order_id:<10} estado={hijo.status}")
print(f"  OP-012 (dentro del subgrupo): {subgrupo.children[0].status}")

seccion("DECORATOR - INSPECCIÓN CON REGISTRO Y MEDICIÓN DE TIEMPO")
timed = TimedInspection(equipment.inspection)
equipment.inspection = LoggedInspection(timed)

resultado = equipment.run_inspection(plantilla)
print(f"Resultado de la inspección: {resultado}")
print(f"Duración medida: {timed.last_duration:.6f} s")
