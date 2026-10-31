import pytest

from src.commands.command import Command, UndoNotSupportedError
from src.commands.invoker import CommandInvoker
from src.commands.mes_commands import (
    FinishOrderCommand,
    ProcessOrderCommand,
    RegisterBatchCommand,
    RegisterOrderCommand,
    RunOrderCommand,
    StartCellCommand,
    StopCellCommand,
)
from src.facade.mes_facade import MESFacade
from src.production.prod_service import ProductionService
from src.production.prod_service_proxy import ProductionServiceProxy


class FakeLogger:
    def __init__(self):
        self.records = []

    def log(self, message, level="INFO"):
        self.records.append((level, message))


@pytest.fixture
def setup():
    logger = FakeLogger()
    return MESFacade(), CommandInvoker(logger=logger), logger


# ---- interfaz Command ------------------------------------------------------
def test_command_is_abstract():
    with pytest.raises(TypeError):
        Command()


def test_commands_are_not_undoable_by_default(setup):
    mes, _, _ = setup
    for cmd in (RegisterOrderCommand(mes, "C-1", "A", 1),
                RegisterBatchCommand(mes, "B-1", "L", [("C-2", "A", 1)]),
                RunOrderCommand(mes, "C-1"),
                FinishOrderCommand(mes, "C-1"),
                ProcessOrderCommand(mes, "C-1")):
        assert cmd.undoable is False
        with pytest.raises(UndoNotSupportedError):
            cmd.undo()


def test_descriptions_identify_each_command(setup):
    mes, _, _ = setup
    assert RegisterOrderCommand(mes, "C-1", "A", 1).description == "Registrar orden C-1"
    assert RegisterBatchCommand(mes, "B-1", "L", []).description == "Registrar lote B-1"
    assert RunOrderCommand(mes, "C-1").description == "Iniciar orden C-1"
    assert FinishOrderCommand(mes, "C-1").description == "Finalizar orden C-1"
    assert ProcessOrderCommand(mes, "C-1").description == "Procesar orden C-1"
    assert StartCellCommand(mes).description == "Iniciar equipo"
    assert StopCellCommand(mes).description == "Detener equipo"


# ---- comandos concretos ----------------------------------------------------
def test_register_order_command(setup):
    mes, invoker, _ = setup
    invoker.execute(RegisterOrderCommand(mes, "C-1", "Pieza A", 10, urgent=True))
    assert mes.production.get_order("C-1").get_priority_score() == 10


def test_register_order_command_passes_builder_options(setup):
    mes, invoker, _ = setup
    invoker.execute(RegisterOrderCommand(mes, "C-1", "Pieza A", 10, lote="L-9"))
    assert mes.production.get_order("C-1").lote == "L-9"


def test_register_batch_command(setup):
    mes, invoker, _ = setup
    group = invoker.execute(RegisterBatchCommand(
        mes, "B-1", "L-1", [("C-1", "A", 1), ("C-2", "B", 2)]))
    assert mes.production.get_order("B-1") is group
    assert mes.get_status_report()["total_ordenes"] == 1


def test_run_command_starts_equipment_and_order(setup):
    mes, invoker, _ = setup
    mes.register_order("C-1", "Pieza A", 10)
    invoker.execute(RunOrderCommand(mes, "C-1"))
    assert mes.production.get_order("C-1").status == "En producción"
    assert mes.equipment.equipment.status == "Operando"


def test_finish_command_returns_facade_result(setup):
    mes, invoker, _ = setup
    mes.register_order("C-1", "Pieza A", 10)
    invoker.execute(RunOrderCommand(mes, "C-1"))
    assert invoker.execute(FinishOrderCommand(mes, "C-1")) is True
    assert mes.production.get_order("C-1").status == "Completada"


def test_process_order_command(setup):
    mes, invoker, _ = setup
    mes.register_order("C-1", "Pieza A", 10)
    assert invoker.execute(ProcessOrderCommand(mes, "C-1")) is True
    assert mes.production.get_order("C-1").status == "Completada"


def test_cell_commands_start_and_stop(setup):
    mes, invoker, _ = setup
    invoker.execute(StartCellCommand(mes))
    assert mes.equipment.equipment.status == "Operando"
    invoker.execute(StopCellCommand(mes))
    assert mes.equipment.equipment.status != "Operando"


# ---- historial y log -------------------------------------------------------
def test_history_records_success_and_failure(setup):
    mes, invoker, logger = setup
    invoker.execute(RegisterOrderCommand(mes, "C-1", "Pieza A", 10))
    with pytest.raises(ValueError):
        invoker.execute(RunOrderCommand(mes, "NO-EXISTE"))
    assert [h["estado"] for h in invoker.history] == ["EJECUTADO", "FALLIDO"]
    assert "no encontrada" in invoker.history[1]["error"]
    assert logger.records[0][0] == "INFO"
    assert logger.records[-1][0] == "WARNING"


def test_history_is_read_only(setup):
    _, invoker, _ = setup
    assert isinstance(invoker.history, tuple)


# ---- ejecución diferida ----------------------------------------------------
def test_deferred_queue_runs_in_order_and_continues_after_failure(setup):
    mes, invoker, _ = setup
    invoker.enqueue(RegisterOrderCommand(mes, "C-1", "Pieza A", 10))
    invoker.enqueue(RunOrderCommand(mes, "NO-EXISTE"))
    invoker.enqueue(ProcessOrderCommand(mes, "C-1"))

    assert len(invoker.pending) == 3
    assert mes.production.get_order("C-1") is None  # nada se ejecutó aún

    entries = invoker.run_pending()

    assert [e["estado"] for e in entries] == ["EJECUTADO", "FALLIDO", "EJECUTADO"]
    assert invoker.pending == ()
    assert mes.production.get_order("C-1").status == "Completada"


def test_run_pending_with_empty_queue(setup):
    _, invoker, _ = setup
    assert invoker.run_pending() == []


def test_command_can_be_reused(setup):
    mes, invoker, _ = setup
    cmd = StartCellCommand(mes)
    invoker.execute(cmd)
    invoker.execute(cmd)
    assert len(invoker.history) == 2


# ---- undo ------------------------------------------------------------------
def test_undo_start_cell(setup):
    mes, invoker, _ = setup
    invoker.execute(StartCellCommand(mes))
    invoker.undo_last()
    assert mes.equipment.equipment.status != "Operando"
    assert invoker.history[-1]["estado"] == "DESHECHO"


def test_undo_stop_cell(setup):
    mes, invoker, _ = setup
    mes.start_cell()
    invoker.execute(StopCellCommand(mes))
    invoker.undo_last()
    assert mes.equipment.equipment.status == "Operando"


def test_undo_is_refused_when_equipment_was_already_running(setup):
    mes, invoker, _ = setup
    mes.start_cell()
    invoker.execute(StartCellCommand(mes))
    with pytest.raises(UndoNotSupportedError):
        invoker.undo_last()
    assert mes.equipment.equipment.status == "Operando"


def test_undo_is_refused_when_orders_are_in_production(setup):
    mes, invoker, _ = setup
    mes.register_order("C-1", "Pieza A", 10)
    invoker.execute(StartCellCommand(mes))
    invoker.execute(RunOrderCommand(mes, "C-1"))
    with pytest.raises(UndoNotSupportedError):
        invoker.undo_last()
    assert mes.equipment.equipment.status == "Operando"
    assert mes.production.get_order("C-1").status == "En producción"


def test_refused_undo_keeps_the_command_in_the_stack(setup):
    mes, invoker, _ = setup
    mes.register_order("C-1", "Pieza A", 10)
    invoker.execute(StartCellCommand(mes))
    invoker.execute(RunOrderCommand(mes, "C-1"))
    with pytest.raises(UndoNotSupportedError):
        invoker.undo_last()
    mes.production.complete_order("C-1")
    invoker.undo_last()  # ahora sí es seguro
    assert mes.equipment.equipment.status != "Operando"


def test_undo_without_undoable_commands(setup):
    mes, invoker, _ = setup
    with pytest.raises(UndoNotSupportedError):
        invoker.undo_last()
    invoker.execute(RegisterOrderCommand(mes, "C-1", "Pieza A", 10))
    with pytest.raises(UndoNotSupportedError):
        invoker.undo_last()


def test_undo_before_execute_is_rejected(setup):
    mes, _, _ = setup
    with pytest.raises(UndoNotSupportedError):
        StartCellCommand(mes).undo()
    with pytest.raises(UndoNotSupportedError):
        StopCellCommand(mes).undo()


# ---- integración con Proxy -------------------------------------------------
def test_commands_respect_the_proxy_roles():
    proxy = ProductionServiceProxy(
        ProductionService(), "visita", "consulta", logger=FakeLogger()
    )
    mes = MESFacade(production_service=proxy)
    invoker = CommandInvoker(logger=FakeLogger())
    with pytest.raises(PermissionError):
        invoker.execute(RegisterOrderCommand(mes, "C-1", "Pieza A", 10))
    assert invoker.history[0]["estado"] == "FALLIDO"
    assert proxy.audit[0]["permitido"] is False


def test_commands_work_through_a_supervisor_proxy():
    proxy = ProductionServiceProxy(
        ProductionService(), "ana", "supervisor", logger=FakeLogger()
    )
    mes = MESFacade(production_service=proxy)
    invoker = CommandInvoker(logger=FakeLogger())
    invoker.execute(RegisterOrderCommand(mes, "C-1", "Pieza A", 10))
    assert invoker.execute(ProcessOrderCommand(mes, "C-1")) is True
    assert [r["operacion"] for r in proxy.audit][0] == "add_order"
