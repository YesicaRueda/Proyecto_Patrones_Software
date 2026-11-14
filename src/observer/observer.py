"""Patrón Observer: eventos del MES, interfaz Observer y Subject.

El Subject notifica a sus observadores suscritos cada vez que ocurre un
evento de planta (equipo, orden, inspección), sin conocer qué hacen con él.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Iterable, Mapping, Optional

from src.infrastructure.logger import Logger


class EventType:
    """Tipos de evento que publica el MES."""

    CELL_STARTED = "CELL_STARTED"
    CELL_STOPPED = "CELL_STOPPED"
    ORDER_STARTED = "ORDER_STARTED"
    ORDER_COMPLETED = "ORDER_COMPLETED"
    INSPECTION_APPROVED = "INSPECTION_APPROVED"
    INSPECTION_REJECTED = "INSPECTION_REJECTED"

    ALL = (
        CELL_STARTED,
        CELL_STOPPED,
        ORDER_STARTED,
        ORDER_COMPLETED,
        INSPECTION_APPROVED,
        INSPECTION_REJECTED,
    )


@dataclass(frozen=True)
class MESEvent:
    """Evento inmutable: tipo, instante, orden involucrada y datos extra."""

    type: str
    timestamp: float
    order_id: Optional[str] = None
    data: Mapping = field(default_factory=lambda: MappingProxyType({}))


class Observer(ABC):
    """Interfaz que implementan los observadores."""

    @abstractmethod
    def update(self, event: MESEvent) -> None:
        ...


class Subject:
    """Mantiene las suscripciones y notifica los eventos."""

    def __init__(self, logger=None):
        self._subscriptions = []  # lista de (observer, frozenset | None)
        self._logger = logger

    @property
    def observers(self):
        return tuple(observer for observer, _ in self._subscriptions)

    def attach(self, observer: Observer,
               event_types: Optional[Iterable[str]] = None) -> None:
        """Suscribe un observador, opcionalmente solo a ciertos tipos."""
        if not isinstance(observer, Observer):
            raise TypeError("El observador debe implementar Observer")
        if any(existing is observer for existing, _ in self._subscriptions):
            raise ValueError("El observador ya está suscrito")
        types = None
        if event_types is not None:
            types = frozenset(event_types)
            if not types:
                raise ValueError("event_types no puede estar vacío")
            unknown = types - set(EventType.ALL)
            if unknown:
                raise ValueError(f"Tipos de evento desconocidos: {sorted(unknown)}")
        self._subscriptions.append((observer, types))

    def detach(self, observer: Observer) -> None:
        for i, (existing, _) in enumerate(self._subscriptions):
            if existing is observer:
                del self._subscriptions[i]
                return
        raise ValueError("El observador no está suscrito")

    def notify(self, event: MESEvent) -> None:
        """Entrega el evento; un observador que falle no afecta a los demás."""
        for observer, types in tuple(self._subscriptions):
            if types is not None and event.type not in types:
                continue
            try:
                observer.update(event)
            except Exception as exc:  # aislamiento de fallos
                self._log(
                    f"Observador {type(observer).__name__} falló al recibir "
                    f"{event.type}: {exc}",
                    "WARNING",
                )

    def _log(self, message, level="INFO"):
        logger = self._logger or Logger.getInstance()
        logger.log(message, level)
