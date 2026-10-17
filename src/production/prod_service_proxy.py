from types import MappingProxyType

from src.infrastructure.logger import Logger

# Operaciones de lectura: pueden usarlas todos los roles.
LECTURA = frozenset({"get_order", "get_pending_queue", "orders"})

# Operaciones que cambian el estado de la producción: se auditan.
ESCRITURA = frozenset({
    "add_order",
    "start_order",
    "start_order_with_equipment",
    "complete_order",
})

PERMISOS = {
    "consulta": LECTURA,
    "operador": LECTURA | {
        "start_order",
        "start_order_with_equipment",
        "complete_order",
    },
    "supervisor": LECTURA | ESCRITURA,
}


class ProductionServiceProxy:
    """Proxy de protección para ProductionService.

    Expone la misma interfaz pública que ProductionService, de modo que
    MESFacade (o cualquier cliente) puede recibirlo en su lugar. Antes de
    delegar cada operación en el servicio real:

    * verifica que el rol del usuario tenga permiso;
    * registra en el Logger y en `audit` quién ejecutó o intentó ejecutar
      cada operación que modifica la producción.

    ProductionService no se modifica y puede seguir usándose directamente.
    Los roles son simulados: no hay autenticación real.
    """

    def __init__(self, service, usuario, rol, logger=None):
        if rol not in PERMISOS:
            raise ValueError(
                f"Rol desconocido: '{rol}'. Roles válidos: {sorted(PERMISOS)}"
            )

        self._service = service
        self.usuario = usuario
        self.rol = rol
        self._logger = logger
        self.audit = []

    # ---- control de acceso -------------------------------------------
    def _authorize(self, operacion, detalle=""):
        permitido = operacion in PERMISOS[self.rol]

        if permitido and operacion not in ESCRITURA:
            return  # las lecturas permitidas no se auditan

        logger = self._logger or Logger.getInstance()
        quien = f"{self.usuario} (rol {self.rol})"
        accion = f"{operacion} {detalle}".strip()

        self.audit.append({
            "usuario": self.usuario,
            "rol": self.rol,
            "operacion": operacion,
            "detalle": detalle,
            "permitido": permitido,
        })

        if not permitido:
            logger.log(f"Acceso denegado: {quien} intentó {accion}", "WARNING")
            raise PermissionError(
                f"El usuario '{self.usuario}' (rol '{self.rol}') "
                f"no tiene permiso para '{operacion}'"
            )

        logger.log(f"Auditoría: {quien} ejecuta {accion}")

    # ---- interfaz de ProductionService --------------------------------
    @property
    def orders(self):
        self._authorize("orders")
        # Vista de solo lectura: el cliente no puede agregar ni quitar
        # órdenes modificando el diccionario del servicio real.
        return MappingProxyType(self._service.orders)

    def add_order(self, order):
        self._authorize("add_order", order.order_id)
        return self._service.add_order(order)

    def get_order(self, order_id):
        self._authorize("get_order", order_id)
        return self._service.get_order(order_id)

    def start_order(self, order_id):
        self._authorize("start_order", order_id)
        return self._service.start_order(order_id)

    def start_order_with_equipment(self, order_id, equipment_service):
        self._authorize("start_order_with_equipment", order_id)
        return self._service.start_order_with_equipment(
            order_id, equipment_service
        )

    def complete_order(self, order_id):
        self._authorize("complete_order", order_id)
        return self._service.complete_order(order_id)

    def get_pending_queue(self):
        self._authorize("get_pending_queue")
        return self._service.get_pending_queue()
