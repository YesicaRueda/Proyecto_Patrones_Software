from src.commands.command import Command, UndoNotSupportedError


class _FacadeCommand(Command):
    """Base de los comandos concretos. El Receiver es `MESFacade`.

    Los comandos no repiten validaciones ni reglas de negocio: llaman a la
    fachada, que a su vez usa ProductionService (o el Proxy que reciba).
    """

    def __init__(self, facade):
        self._facade = facade


# ---- registro ---------------------------------------------------------
class RegisterOrderCommand(_FacadeCommand):
    def __init__(self, facade, order_id, product, quantity,
                 urgent=False, **options):
        super().__init__(facade)
        self._order_id = order_id
        self._args = (order_id, product, quantity)
        self._urgent = urgent
        self._options = options

    @property
    def description(self):
        return f"Registrar orden {self._order_id}"

    def execute(self):
        return self._facade.register_order(
            *self._args, urgent=self._urgent, **self._options
        )


class RegisterBatchCommand(_FacadeCommand):
    def __init__(self, facade, batch_id, lote, items, urgent=False):
        super().__init__(facade)
        self._batch_id = batch_id
        self._lote = lote
        self._items = list(items)
        self._urgent = urgent

    @property
    def description(self):
        return f"Registrar lote {self._batch_id}"

    def execute(self):
        return self._facade.register_batch(
            self._batch_id, self._lote, self._items, self._urgent
        )


# ---- ciclo de vida de una orden ----------------------------------------
class _OrderCommand(_FacadeCommand):
    verbo = ""

    def __init__(self, facade, order_id):
        super().__init__(facade)
        self._order_id = order_id

    @property
    def description(self):
        return f"{self.verbo} orden {self._order_id}"


class RunOrderCommand(_OrderCommand):
    verbo = "Iniciar"

    def execute(self):
        return self._facade.run_order(self._order_id)


class FinishOrderCommand(_OrderCommand):
    verbo = "Finalizar"

    def execute(self):
        return self._facade.finish_order(self._order_id)


class ProcessOrderCommand(_OrderCommand):
    verbo = "Procesar"

    def execute(self):
        return self._facade.process_order(self._order_id)


# ---- equipo (únicos comandos con undo seguro) ---------------------------
class _CellCommand(_FacadeCommand):
    undoable = True

    def __init__(self, facade):
        super().__init__(facade)
        self._was_running = None

    def _running(self):
        return self._facade.equipment.equipment.status == "Operando"

    def _orders_in_production(self):
        return [o.order_id for o in self._facade.production.orders.values()
                if o.status == "En producción"]


class StartCellCommand(_CellCommand):
    description = "Iniciar equipo"

    def execute(self):
        self._was_running = self._running()
        self._facade.start_cell()

    def undo(self):
        if self._was_running is None:
            raise UndoNotSupportedError("el comando todavía no se ejecutó")
        if self._was_running:
            raise UndoNotSupportedError(
                "el equipo ya estaba operando antes del comando"
            )
        en_produccion = self._orders_in_production()
        if en_produccion:
            raise UndoNotSupportedError(
                f"hay órdenes en producción: {en_produccion}"
            )
        self._facade.stop_cell()


class StopCellCommand(_CellCommand):
    description = "Detener equipo"

    def execute(self):
        self._was_running = self._running()
        self._facade.stop_cell()

    def undo(self):
        if self._was_running is None:
            raise UndoNotSupportedError("el comando todavía no se ejecutó")
        if not self._was_running:
            raise UndoNotSupportedError(
                "el equipo no estaba operando antes del comando"
            )
        self._facade.start_cell()
