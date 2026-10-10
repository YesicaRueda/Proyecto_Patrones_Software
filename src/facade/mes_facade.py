from src.equipment.cell_factory import (
    AbstractProductionCellFactory,
    CNCCellFactory,
)
from src.equipment.equipment_service import EquipmentService
from src.infrastructure.logger import Logger
from src.production.order_builder import OrderBuilder
from src.production.order_group import OrderGroup
from src.production.prod_factory import (
    StandardOrderCreator,
    UrgentOrderCreator,
)
from src.production.prod_service import ProductionService


class MESFacade:
    """Facade: interfaz simple para operar el MES.

    Coordina ProductionService, EquipmentService, las fábricas, el Builder,
    el Composite y el Logger, de modo que el cliente no tenga que conocer ni
    ordenar los pasos de cada subsistema.

    La fachada no oculta los subsistemas: `production` y `equipment` siguen
    siendo accesibles para quien necesite una operación más específica.
    """

    def __init__(
        self,
        cell_factory: AbstractProductionCellFactory = None,
        production_service: ProductionService = None,
        equipment_service: EquipmentService = None,
    ):
        self.production = production_service or ProductionService()
        self.equipment = equipment_service or EquipmentService(
            cell_factory or CNCCellFactory()
        )
        self._standard_creator = StandardOrderCreator()
        self._urgent_creator = UrgentOrderCreator()

    # ---- equipo ------------------------------------------------------
    def start_cell(self):
        """Pone el equipo en operación si todavía no lo está."""
        if self.equipment.equipment.status != "Operando":
            self.equipment.start_machine()

    def stop_cell(self):
        self.equipment.stop_machine()

    # ---- registro de órdenes -----------------------------------------
    def _create_order(self, order_id, product, quantity, urgent, **options):
        data = OrderBuilder(order_id, product, quantity)

        if options.get("lote") is not None:
            data.with_lote(options["lote"])
        if options.get("fecha_ingreso") is not None:
            data.with_fecha_ingreso(options["fecha_ingreso"])
        if options.get("fecha_entrega") is not None:
            data.with_fecha_entrega(options["fecha_entrega"])
        if options.get("descripcion") is not None:
            data.with_descripcion(options["descripcion"])
        if options.get("equipo_asignado") is not None:
            data.with_equipo_asignado(options["equipo_asignado"])

        creator = self._urgent_creator if urgent else self._standard_creator
        return creator.create_order(data.build())

    def register_order(self, order_id, product, quantity, urgent=False, **options):
        """Construye (Builder), crea (Factory Method) y registra una orden.

        `options` admite: lote, fecha_ingreso, fecha_entrega, descripcion
        y equipo_asignado.
        """
        order = self._create_order(order_id, product, quantity, urgent, **options)
        self.production.add_order(order)
        return order

    def register_batch(self, batch_id, lote, items, urgent=False):
        """Registra un lote como un único grupo de órdenes (Composite).

        `items` es una lista de tuplas (order_id, product, quantity).
        El grupo se arma completo antes de registrarse, de modo que si algún
        elemento es inválido no queda nada registrado.
        """
        items = list(items)
        if not items:
            raise ValueError(f"El lote {batch_id} debe tener al menos una orden")

        group = OrderGroup(batch_id, lote=lote)
        for order_id, product, quantity in items:
            group.add(
                self._create_order(order_id, product, quantity, urgent, lote=lote)
            )

        self.production.add_order(group)
        return group

    # ---- ciclo de vida de una orden ----------------------------------
    def run_order(self, order_id):
        """Pone el equipo en operación (si hace falta) e inicia la orden."""
        self.start_cell()
        self.production.start_order_with_equipment(order_id, self.equipment)

    def finish_order(self, order_id) -> bool:
        """Inspecciona la orden y, si la inspección es aprobada, la completa.

        Devuelve False (y deja la orden en producción) si la inspección
        es rechazada.
        """
        order = self.production.get_order(order_id)

        if order is None:
            raise ValueError(f"Orden {order_id} no encontrada")

        if order.status != "En producción":
            raise ValueError(
                f"La orden {order_id} no se puede finalizar porque su estado "
                f"es '{order.status}'"
            )

        if not self.equipment.run_inspection(order):
            Logger.getInstance().log(
                f"Orden {order_id} no completada: inspección rechazada",
                "WARNING",
            )
            return False

        self.production.complete_order(order_id)
        return True

    def process_order(self, order_id) -> bool:
        """Flujo completo: iniciar, inspeccionar y completar la orden."""
        self.run_order(order_id)
        return self.finish_order(order_id)

    # ---- consulta ----------------------------------------------------
    def get_status_report(self) -> dict:
        """Resumen del estado del equipo, las órdenes y la cola pendiente."""
        orders = list(self.production.orders.values())
        counts = {"Pendiente": 0, "En producción": 0, "Completada": 0}
        for order in orders:
            counts[order.status] = counts.get(order.status, 0) + 1

        return {
            "equipo": type(self.equipment.equipment).__name__,
            "estado_equipo": self.equipment.equipment.status,
            "ordenes": counts,
            "total_ordenes": len(orders),
            "cola_pendiente": [
                {"order_id": o.order_id, "prioridad": o.get_priority_score()}
                for o in self.production.get_pending_queue()
            ],
        }
