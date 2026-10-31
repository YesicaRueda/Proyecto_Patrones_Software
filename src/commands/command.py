from abc import ABC, abstractmethod


class UndoNotSupportedError(Exception):
    """El comando no se puede deshacer de forma segura."""


class Command(ABC):
    """Command: una solicitud del MES encapsulada como objeto.

    Cada comando concreto sabe qué operación pedir y con qué datos, pero no
    la implementa: la delega en el Receiver (MESFacade). Por defecto un
    comando no es reversible; solo lo es si el dominio permite deshacerlo
    de forma segura (`undoable = True` y `undo()` implementado).
    """

    undoable = False

    @property
    @abstractmethod
    def description(self) -> str:
        """Texto legible que identifica el comando en el historial y el log."""

    @abstractmethod
    def execute(self):
        """Ejecuta la operación y devuelve el resultado de la fachada."""

    def undo(self):
        raise UndoNotSupportedError(
            f"'{self.description}' no se puede deshacer de forma segura"
        )
