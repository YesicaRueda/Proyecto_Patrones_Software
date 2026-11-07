from src.infrastructure.logger import Logger
from src.production.prod_service import ProductionService
from src.production.prod_service_proxy import ProductionServiceProxy
from src.equipment.equipment_service import EquipmentService
from src.equipment.cell_factory import CNCCellFactory, RobotCellFactory
from src.production.prod_factory import (
    StandardOrderCreator,
    UrgentOrderCreator
)
from datetime import datetime
from src.production.order_builder import OrderBuilder
from src.production.order_group import OrderGroup
from src.production.order_iterators import create_iterator, leaf_status_counts
from src.facade.mes_facade import MESFacade
from src.production.prod_order import StandardOrder
from src.equipment.inspection_decorators import (
    LoggedInspection,
    TimedInspection
)
from src.commands.invoker import CommandInvoker
from src.commands.mes_commands import (
    ProcessOrderCommand,
    RegisterOrderCommand,
    RunOrderCommand,
    StartCellCommand,
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

seccion("FACADE - OPERACIÓN SIMPLIFICADA DEL MES")
mes = MESFacade(RobotCellFactory())

mes.register_order("F-001", "Ensamble A", 10, urgent=True, lote="L-2026-10")
mes.register_batch(
    "F-LOTE", "L-2026-10",
    [("F-002", "Ensamble B", 20), ("F-003", "Ensamble C", 30)]
)


def mostrar_reporte(titulo, reporte):
    print(f"{titulo}: equipo={reporte['equipo']} ({reporte['estado_equipo']}), "
          f"órdenes={reporte['ordenes']}")


mostrar_reporte("Antes", mes.get_status_report())

print(f"Orden F-001 procesada: {mes.process_order('F-001')}")
print(f"Lote F-LOTE procesado: {mes.process_order('F-LOTE')}")

mostrar_reporte("Después", mes.get_status_report())

seccion("PROXY - CONTROL DE ACCESO Y AUDITORÍA")
servicio_real = ProductionService()
supervisor = ProductionServiceProxy(servicio_real, "ana", "supervisor")
operador = ProductionServiceProxy(servicio_real, "luis", "operador")
consulta = ProductionServiceProxy(servicio_real, "visita", "consulta")

supervisor.add_order(StandardOrder("P-001", "Pieza P", 5))

for proxy in (operador, consulta):
    try:
        proxy.add_order(StandardOrder("P-002", "Pieza Q", 5))
    except PermissionError as error:
        print(f"Denegado: {error}")

operador.start_order("P-001")
operador.complete_order("P-001")
print(f"Estado de P-001 tras operarla el operador: "
      f"{servicio_real.get_order('P-001').status}")

try:
    consulta.start_order("P-001")
except PermissionError as error:
    print(f"Denegado: {error}")

print("Auditoría del operador:",
      [(r["operacion"], r["permitido"]) for r in operador.audit])
print("Auditoría de consulta:",
      [(r["operacion"], r["permitido"]) for r in consulta.audit])

mes_consulta = MESFacade(production_service=consulta)
try:
    mes_consulta.register_order("P-009", "Pieza X", 1)
except PermissionError as error:
    print(f"Fachada con rol de consulta: {error}")
print(f"Órdenes visibles para consulta: "
      f"{mes_consulta.get_status_report()['total_ordenes']}")

seccion("COMMAND - EJECUCIÓN DE OPERACIONES")
mes_cmd = MESFacade(CNCCellFactory())
invoker = CommandInvoker()

print("Turno planificado (cola diferida; todavía no se ejecuta nada):")
invoker.enqueue(RegisterOrderCommand(mes_cmd, "C-001", "Pieza A", 10, urgent=True))
invoker.enqueue(RunOrderCommand(mes_cmd, "C-999"))  # orden inexistente
invoker.enqueue(ProcessOrderCommand(mes_cmd, "C-001"))
print(f"  Pendientes: {[c.description for c in invoker.pending]}")
print(f"  Órdenes registradas antes de ejecutar: "
      f"{mes_cmd.get_status_report()['total_ordenes']}")

print("Ejecutando la cola:")
for entrada in invoker.run_pending():
    resultado = entrada["resultado"]
    detalle = entrada["error"] or getattr(resultado, "order_id", resultado)
    print(f"  {entrada['comando']:<24} {entrada['estado']:<10} {detalle}")

print("Undo seguro sobre el equipo:")
mes_cmd.stop_cell()
invoker.execute(StartCellCommand(mes_cmd))
print(f"  Tras 'Iniciar equipo': {mes_cmd.equipment.equipment.status}")
invoker.undo_last()
print(f"  Tras deshacer:         {mes_cmd.equipment.equipment.status}")

print(f"Historial completo: {len(invoker.history)} entradas")
for h in invoker.history:
    print(f"  - {h['comando']}: {h['estado']}")

seccion("ITERATOR - RECORRIDO DE UN LOTE")
lote_it = OrderGroup("LOTE-IT", lote="L-2026-11")
sub_it = OrderGroup("SUB-IT", lote="L-2026-11")
lote_it.add(StandardOrder("IT-001", "Pieza A", 10))
sub_it.add(urgent_creator.create_order(OrderBuilder("IT-002", "Pieza B", 5).build()))
sub_it.add(StandardOrder("IT-003", "Pieza C", 8))
lote_it.add(sub_it)
lote_it.add(StandardOrder("IT-004", "Pieza D", 12))

print("En profundidad:", [o.order_id for o in create_iterator(lote_it)])
print("Por niveles   :", [o.order_id for o in create_iterator(lote_it, "breadth")])
print("Con grupos    :",
      [o.order_id for o in create_iterator(lote_it, leaves_only=False)])

sub_it.start()
print("En producción :",
      [o.order_id for o in create_iterator(lote_it, status="En producción")])
print("Hojas por estado:", leaf_status_counts([lote_it]))

print(f"Órdenes registradas en el servicio: {len(production.orders)}")
print(f"Órdenes individuales (hojas): "
      f"{sum(leaf_status_counts(production.orders.values()).values())}")
print("Hojas por estado:", leaf_status_counts(production.orders.values()))
