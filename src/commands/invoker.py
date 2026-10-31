from collections import deque

from src.commands.command import UndoNotSupportedError
from src.infrastructure.logger import Logger


class CommandInvoker:
    """Invoker: ejecuta, encola, registra y (si es seguro) deshace comandos.

    * `execute()` ejecuta de inmediato y deja constancia en el historial y
      en el Logger (WARNING si el comando falla).
    * `enqueue()` + `run_pending()` permiten ejecución diferida (FIFO); un
      fallo no detiene los comandos siguientes.
    * `undo_last()` solo deshace comandos reversibles y es seguro: si el
      comando rechaza el undo, se conserva en la pila.
    """

    def __init__(self, logger=None):
        self._logger = logger
        self._queue = deque()
        self._history = []
        self._undo_stack = []

    @property
    def history(self):
        return tuple(self._history)

    @property
    def pending(self):
        return tuple(self._queue)

    def _log(self, message, level="INFO"):
        (self._logger or Logger.getInstance()).log(message, level)

    def _record(self, command, estado, resultado=None, error=None):
        self._history.append({
            "comando": command.description,
            "estado": estado,
            "resultado": resultado,
            "error": error,
        })

    def execute(self, command):
        try:
            result = command.execute()
        except Exception as error:
            self._record(command, "FALLIDO", error=str(error))
            self._log(
                f"Comando fallido: {command.description}: {error}", "WARNING"
            )
            raise
        self._record(command, "EJECUTADO", resultado=result)
        self._log(f"Comando ejecutado: {command.description}")
        if command.undoable:
            self._undo_stack.append(command)
        return result

    def enqueue(self, command):
        self._queue.append(command)

    def run_pending(self):
        """Ejecuta la cola en orden; devuelve las entradas del historial."""
        entries = []
        while self._queue:
            try:
                self.execute(self._queue.popleft())
            except Exception:
                pass  # ya quedó registrado como FALLIDO
            entries.append(self._history[-1])
        return entries

    def undo_last(self):
        if not self._undo_stack:
            raise UndoNotSupportedError(
                "No hay comandos que se puedan deshacer"
            )
        command = self._undo_stack[-1]
        command.undo()  # si no es seguro lanza y el comando se conserva
        self._undo_stack.pop()
        self._record(command, "DESHECHO")
        self._log(f"Comando deshecho: {command.description}")
