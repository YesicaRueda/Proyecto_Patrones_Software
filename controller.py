"""Controlador de la visual del MES (sin dependencias de interfaz).

Conecta una pantalla con el proyecto real: crea una `ObservableMESFacade`,
suscribe observadores reales y registra una traza de lo que ocurre por
debajo (llamadas, eventos y entrega a cada observador). No modifica ninguna
clase existente: la traza se obtiene con una subclase y un envoltorio.
"""
import threading
import time

from src.equipment.cell_factory import CNCCellFactory, RobotCellFactory
from src.equipment.equipment_base import Inspection
from src.observer.observable_facade import ObservableMESFacade
from src.observer.observer import EventType, Observer
from src.observer.observers import ProductionMetricsObserver, RejectionAlertObserver

MAX_TRACE = 600
LINES = {"cnc": ("Línea CNC", CNCCellFactory), "robot": ("Línea robótica", RobotCellFactory)}


def _short(value):
    """Representación corta y legible de un argumento para la traza."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return repr(value)
    label = getattr(value, "_label", None)  # servicio envuelto por _CallTracer
    if isinstance(label, str):
        return label
    order_id = getattr(value, "order_id", None)
    if isinstance(order_id, str):
        return f"{type(value).__name__}({order_id!r})"
    return type(value).__name__


def _args(args, kwargs):
    parts = [_short(a) for a in args] + [f"{k}={_short(v)}" for k, v in kwargs.items()]
    return ", ".join(parts)


class Trace:
    """Bitácora cronológica con número de secuencia."""

    def __init__(self):
        self.t0 = time.monotonic()
        self.seq = 0
        self.entries = []
        self.depth = 0

    def add(self, kind, text, **extra):
        self.seq += 1
        entry = {"seq": self.seq, "t": round(time.monotonic() - self.t0, 3),
                 "kind": kind, "text": text, "depth": self.depth, **extra}
        self.entries.append(entry)
        if len(self.entries) > MAX_TRACE:
            del self.entries[: len(self.entries) - MAX_TRACE]
        return entry

    def since(self, seq):
        return [e for e in self.entries if e["seq"] > seq]


class _CallTracer:
    """Envuelve un servicio y anota cada llamada a un método (no las lecturas)."""

    def __init__(self, target, label, trace):
        object.__setattr__(self, "_target", target)
        object.__setattr__(self, "_label", label)
        object.__setattr__(self, "_trace", trace)

    def __getattr__(self, name):
        attr = getattr(self._target, name)
        if not callable(attr) or name.startswith(("_", "get_")):
            return attr
        trace, label = self._trace, self._label

        def traced(*args, **kwargs):
            call = f"{label}.{name}({_args(args, kwargs)})"
            trace.add("call", call)
            trace.depth += 1
            try:
                result = attr(*args, **kwargs)
            except Exception as exc:
                trace.depth -= 1
                trace.add("error", f"{type(exc).__name__}: {exc}")
                raise
            trace.depth -= 1
            trace.add("return", "listo" if result is None else repr(result))
            return result

        return traced

    def __setattr__(self, name, value):
        setattr(self._target, name, value)


class _TracedFacade(ObservableMESFacade):
    """ObservableMESFacade que además anota sus operaciones y cada entrega."""

    def __init__(self, factory, trace, **kwargs):
        self._trace = trace
        self._filters = {}
        self.rejected = set()
        super().__init__(factory, **kwargs)

    # --- suscripciones: se recuerda el filtro para mostrar "entregado/filtrado"
    def attach(self, observer, event_types=None):
        super().attach(observer, event_types)
        self._filters[id(observer)] = None if event_types is None else frozenset(event_types)

    def detach(self, observer):
        super().detach(observer)
        self._filters.pop(id(observer), None)

    def notify(self, event):
        deliveries = []
        for observer in self.observers:
            types = self._filters.get(id(observer))
            delivered = types is None or event.type in types
            deliveries.append({"observer": type(observer).__name__,
                               "status": "delivered" if delivered else "filtered"})
        if event.type == EventType.INSPECTION_REJECTED:
            self.rejected.add(event.order_id)
        elif event.type == EventType.INSPECTION_APPROVED:
            self.rejected.discard(event.order_id)
        self.current_entry = self._trace.add(
            "event", event.type, order_id=event.order_id,
            data=dict(event.data), deliveries=deliveries)
        try:
            super().notify(event)
        finally:
            self.current_entry = None

    # --- operaciones: entrada, salida y errores
    def _traced(self, name, args, kwargs, call):
        trace = self._trace
        trace.add("call", f"MESFacade.{name}({_args(args, kwargs)})")
        trace.depth += 1
        try:
            result = call()
        except Exception as exc:
            trace.depth -= 1
            trace.add("error", f"{type(exc).__name__}: {exc}")
            raise
        trace.depth -= 1
        trace.add("return", "listo" if result is None else repr(result))
        return result

    def register_order(self, *args, **kwargs):
        return self._traced("register_order", args, kwargs,
                            lambda: super(_TracedFacade, self).register_order(*args, **kwargs))

    def start_cell(self, *args, **kwargs):
        return self._traced("start_cell", args, kwargs,
                            lambda: super(_TracedFacade, self).start_cell(*args, **kwargs))

    def stop_cell(self, *args, **kwargs):
        return self._traced("stop_cell", args, kwargs,
                            lambda: super(_TracedFacade, self).stop_cell(*args, **kwargs))

    def run_order(self, *args, **kwargs):
        return self._traced("run_order", args, kwargs,
                            lambda: super(_TracedFacade, self).run_order(*args, **kwargs))

    def finish_order(self, *args, **kwargs):
        return self._traced("finish_order", args, kwargs,
                            lambda: super(_TracedFacade, self).finish_order(*args, **kwargs))

    def process_order(self, *args, **kwargs):
        return self._traced("process_order", args, kwargs,
                            lambda: super(_TracedFacade, self).process_order(*args, **kwargs))


class _GuiLogger:
    """Logger de la visual: lo que el Subject y las alertas escriben va a la traza."""

    def __init__(self, trace, facade_ref):
        self._trace = trace
        self._facade_ref = facade_ref

    def log(self, message, level="INFO"):
        self._trace.add("log", message, level=level)
        facade = self._facade_ref()
        entry = getattr(facade, "current_entry", None)
        if entry and message.startswith("Observador ") and " falló" in message:
            name = message[len("Observador "):].split(" falló")[0]
            for delivery in entry["deliveries"]:
                if delivery["observer"] == name and delivery["status"] == "delivered":
                    delivery["status"] = "failed"


class _RejectingInspection(Inspection):
    def inspect(self, order):
        return False


class _FaultyObserver(Observer):
    """Observador de demostración que siempre falla (para mostrar el aislamiento)."""

    def update(self, event):
        raise RuntimeError("fallo simulado")


class DashboardController:
    def __init__(self, line="cnc"):
        self._lock = threading.RLock()
        self.epoch = 0
        self.reset(line)

    # ------------------------------------------------------------------ setup
    def reset(self, line=None):
        with self._lock:
            if line is not None:
                if line not in LINES:
                    raise ValueError(f"Línea desconocida: {line}")
                self.line = line
            self.epoch += 1
            self.trace = Trace()
            self.counter = 0
            self.reject_next = False
            label, factory = LINES[self.line]
            self.line_label = label
            holder = {}
            logger = _GuiLogger(self.trace, lambda: holder.get("mes"))
            mes = _TracedFacade(factory(), self.trace, logger=logger)
            holder["mes"] = mes
            self.mes = mes
            self._real_inspection = mes.equipment.inspection
            mes.production = _CallTracer(mes.production, "ProductionService", self.trace)
            mes.equipment = _CallTracer(mes.equipment, "EquipmentService", self.trace)

            self.metrics = ProductionMetricsObserver()
            self.alerts = RejectionAlertObserver(logger=logger)
            self.registry = {
                "metrics": {"obj": self.metrics, "types": None,
                            "name": "ProductionMetricsObserver",
                            "desc": "Cuenta y mide: base del OEE"},
                "alerts": {"obj": self.alerts, "types": [EventType.INSPECTION_REJECTED],
                           "name": "RejectionAlertObserver",
                           "desc": "Solo inspecciones rechazadas"},
                "faulty": {"obj": _FaultyObserver(), "types": None,
                           "name": "_FaultyObserver",
                           "desc": "Observador que siempre falla (demo)"},
            }
            for key in ("metrics", "alerts"):
                self._set_subscribed(key, True)
            self.trace.add("log", f"Sistema listo: {label}. Observadores suscritos: métricas y alertas.",
                           level="INFO")

    def _set_subscribed(self, key, on):
        item = self.registry[key]
        subscribed = any(o is item["obj"] for o in self.mes.observers)
        if on and not subscribed:
            self.mes.attach(item["obj"], item["types"])
            self.trace.add("log", f"attach({item['name']})", level="INFO")
        elif not on and subscribed:
            self.mes.detach(item["obj"])
            self.trace.add("log", f"detach({item['name']})", level="INFO")

    # ---------------------------------------------------------------- actions
    def act(self, action, **p):
        """Ejecuta una acción. Devuelve {'ok': bool, ...}; nunca lanza."""
        with self._lock:
            try:
                return {"ok": True, **self._dispatch(action, p)}
            except Exception as exc:  # el error ya quedó en la traza si vino de una operación
                return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    def _dispatch(self, action, p):
        mes = self.mes
        if action == "register":
            self.counter += 1
            order_id = f"OB-{self.counter:03d}"
            try:
                mes.register_order(order_id, p.get("product", "Pieza"), int(p.get("quantity", 1)),
                                   urgent=bool(p.get("urgent", False)))
            except Exception:
                self.counter -= 1
                raise
            return {"order_id": order_id}
        if action == "start_cell":
            mes.start_cell()
        elif action == "stop_cell":
            mes.stop_cell()
        elif action == "run":
            mes.run_order(p["order_id"])
        elif action == "finish":
            return {"approved": mes.finish_order(p["order_id"])}
        elif action == "process":
            return {"approved": mes.process_order(p["order_id"])}
        elif action == "reject_next":
            self.reject_next = bool(p.get("value"))
            mes.equipment.inspection = (_RejectingInspection() if self.reject_next
                                        else self._real_inspection)
            self.trace.add("log", "La próxima inspección " +
                           ("RECHAZARÁ" if self.reject_next else "volverá a aprobar"), level="INFO")
        elif action == "observer":
            self._set_subscribed(p["key"], bool(p["on"]))
        elif action == "reset":
            self.reset(p.get("line"))
        else:
            raise ValueError(f"Acción desconocida: {action}")
        return {}

    # ------------------------------------------------------------------ state
    def state(self, since=0):
        with self._lock:
            mes = self.mes
            now = mes._clock()
            m = self.metrics
            orders = []
            for o in mes.production.orders.values():
                try:
                    priority = o.get_priority_score()
                except Exception:
                    priority = None
                orders.append({"id": getattr(o, "order_id", "?"), "product": getattr(o, "product", ""),
                               "quantity": getattr(o, "quantity", 0), "status": getattr(o, "status", ""),
                               "kind": type(o).__name__, "priority": priority,
                               "rejected": getattr(o, "order_id", None) in mes.rejected})
            cell_status = mes.cell_status()
            operating = cell_status == "Operando"
            return {
                "epoch": self.epoch,
                "line": self.line,
                "line_label": self.line_label,
                "lines": {k: v[0] for k, v in LINES.items()},
                "cell": {"operating": operating, "status": cell_status},
                "orders": orders,
                "kpis": {"started": m.orders_started, "completed": m.orders_completed,
                         "quality": m.quality_rate(), "availability": m.availability(now),
                         "operating_seconds": m.operating_seconds(now)},
                "reject_next": self.reject_next,
                "observers": [{"key": k, "name": v["name"], "desc": v["desc"],
                               "filter": v["types"],
                               "subscribed": any(o is v["obj"] for o in mes.observers)}
                              for k, v in self.registry.items()],
                "trace": self.trace.since(since),
                "next": self.trace.seq,
            }
