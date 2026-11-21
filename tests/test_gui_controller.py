import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

from src.gui.controller import DashboardController
from src.gui.server import make_handler


def events(ctrl, type_=None):
    items = [e for e in ctrl.trace.entries if e["kind"] == "event"]
    return [e for e in items if type_ is None or e["text"] == type_]


def deliveries(entry):
    return {d["observer"]: d["status"] for d in entry["deliveries"]}


def test_initial_state_has_two_observers_and_stopped_cell():
    state = DashboardController().state()
    assert state["cell"]["operating"] is False
    assert [o["key"] for o in state["observers"] if o["subscribed"]] == ["metrics", "alerts"]
    assert state["orders"] == []


def test_process_order_traces_calls_events_and_updates_kpis():
    ctrl = DashboardController()
    order_id = ctrl.act("register", product="Pieza A", quantity=10)["order_id"]
    assert ctrl.act("process", order_id=order_id)["approved"] is True

    texts = [e["text"] for e in ctrl.trace.entries]
    assert any(t.startswith("MESFacade.process_order(") for t in texts)
    assert any(t.startswith("MESFacade.run_order(") for t in texts)
    assert [e["text"] for e in events(ctrl)] == [
        "CELL_STARTED", "ORDER_STARTED", "INSPECTION_APPROVED", "ORDER_COMPLETED"]

    state = ctrl.state()
    assert state["kpis"]["started"] == 1 and state["kpis"]["completed"] == 1
    assert state["kpis"]["quality"] == 1.0
    assert state["orders"][0]["status"] == "Completada"


def test_events_show_who_received_them_and_who_was_filtered():
    ctrl = DashboardController()
    order_id = ctrl.act("register", product="P", quantity=5)["order_id"]
    ctrl.act("reject_next", value=True)
    ctrl.act("process", order_id=order_id)

    started = deliveries(events(ctrl, "ORDER_STARTED")[0])
    rejected = deliveries(events(ctrl, "INSPECTION_REJECTED")[0])
    assert started == {"ProductionMetricsObserver": "delivered", "RejectionAlertObserver": "filtered"}
    assert rejected == {"ProductionMetricsObserver": "delivered", "RejectionAlertObserver": "delivered"}


def test_rejection_flags_order_and_keeps_it_in_production():
    ctrl = DashboardController()
    order_id = ctrl.act("register", product="P", quantity=5)["order_id"]
    ctrl.act("reject_next", value=True)
    assert ctrl.act("process", order_id=order_id)["approved"] is False
    order = ctrl.state()["orders"][0]
    assert order["status"] == "En producción" and order["rejected"] is True
    assert any(e["kind"] == "log" and "ALERTA" in e["text"] for e in ctrl.trace.entries)


def test_detaching_metrics_observer_freezes_the_kpis():
    ctrl = DashboardController()
    ctrl.act("observer", key="metrics", on=False)
    order_id = ctrl.act("register", product="P", quantity=5)["order_id"]
    ctrl.act("process", order_id=order_id)
    assert ctrl.state()["kpis"]["started"] == 0
    ctrl.act("observer", key="metrics", on=True)
    assert [o["subscribed"] for o in ctrl.state()["observers"] if o["key"] == "metrics"] == [True]


def test_faulty_observer_is_marked_failed_without_stopping_the_others():
    ctrl = DashboardController()
    ctrl.act("observer", key="faulty", on=True)
    order_id = ctrl.act("register", product="P", quantity=5)["order_id"]
    assert ctrl.act("process", order_id=order_id)["ok"] is True
    entry = events(ctrl, "ORDER_STARTED")[0]
    assert deliveries(entry)["_FaultyObserver"] == "failed"
    assert deliveries(entry)["ProductionMetricsObserver"] == "delivered"
    assert ctrl.state()["kpis"]["completed"] == 1


def test_failed_operation_returns_error_and_is_traced_without_raising():
    ctrl = DashboardController()
    result = ctrl.act("run", order_id="NO-EXISTE")
    assert result["ok"] is False and "ValueError" in result["error"]
    assert any(e["kind"] == "error" for e in ctrl.trace.entries)
    assert not events(ctrl, "ORDER_STARTED")


def test_unknown_action_is_reported():
    assert DashboardController().act("inexistente")["ok"] is False


def test_trace_since_returns_only_new_entries():
    ctrl = DashboardController()
    cursor = ctrl.state()["next"]
    ctrl.act("start_cell")
    new = ctrl.state(since=cursor)["trace"]
    assert new and all(e["seq"] > cursor for e in new)
    assert ctrl.state(since=ctrl.state()["next"])["trace"] == []


def test_reset_clears_everything_and_changes_epoch():
    ctrl = DashboardController()
    epoch = ctrl.epoch
    order_id = ctrl.act("register", product="P", quantity=5)["order_id"]
    ctrl.act("process", order_id=order_id)
    assert ctrl.act("reset")["ok"] is True
    state = ctrl.state()
    assert ctrl.epoch == epoch + 1 and state["orders"] == [] and state["kpis"]["started"] == 0
    assert ctrl.act("reset", line="no-existe")["ok"] is False


def test_http_server_serves_page_state_and_actions():
    ctrl = DashboardController()
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(ctrl))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        assert b"Observer en vivo" in urllib.request.urlopen(base + "/").read()
        req = urllib.request.Request(
            base + "/api/action", data=json.dumps({"action": "start_cell"}).encode(),
            headers={"Content-Type": "application/json"})
        assert json.load(urllib.request.urlopen(req))["ok"] is True
        state = json.load(urllib.request.urlopen(base + "/api/state?since=0"))
        assert state["cell"]["operating"] is True
        assert any(e["text"] == "CELL_STARTED" for e in state["trace"])
    finally:
        server.shutdown()
        server.server_close()


# ------------------------------------------------ Strategy y Command en la visual
def register(ctrl, quantity, urgent=False, due=None):
    return ctrl.act("register", product="P", quantity=quantity, urgent=urgent, due=due)["order_id"]


def queue_ids(ctrl):
    return [row["id"] for row in ctrl.state()["queue"]]


def test_state_lists_the_four_policies_and_priority_is_the_default():
    state = DashboardController().state()
    assert [s["key"] for s in state["strategies"]] == ["priority", "fifo", "due_date", "smallest"]
    assert state["strategy"] == "priority"


def test_switching_policy_reorders_the_planned_queue_and_is_logged():
    ctrl = DashboardController()
    a = register(ctrl, 40)
    b = register(ctrl, 5, urgent=True)
    c = register(ctrl, 20)
    assert queue_ids(ctrl) == [b, a, c]                       # prioridad
    ctrl.act("strategy", key="fifo")
    assert queue_ids(ctrl) == [a, b, c]
    ctrl.act("strategy", key="smallest")
    assert queue_ids(ctrl) == [b, c, a]
    assert ctrl.state()["strategy"] == "smallest"
    logs = [e["text"] for e in ctrl.trace.entries if e["kind"] == "log"]
    assert any("SmallestFirstStrategy" in t for t in logs)


def test_due_date_policy_uses_the_date_given_when_registering():
    ctrl = DashboardController()
    a = register(ctrl, 10, due="2026-12-30")
    b = register(ctrl, 10, due="2026-12-01")
    c = register(ctrl, 10)
    ctrl.act("strategy", key="due_date")
    assert queue_ids(ctrl) == [b, a, c]
    assert ctrl.state()["queue"][0]["due"] == "2026-12-01"


def test_invalid_date_and_unknown_policy_are_reported_without_side_effects():
    ctrl = DashboardController()
    assert ctrl.act("register", product="P", quantity=1, due="30/12/2026")["ok"] is False
    assert ctrl.state()["orders"] == []
    assert register(ctrl, 1) == "OB-001"                      # el contador no avanzó
    assert ctrl.act("strategy", key="no-existe")["ok"] is False


def test_registering_without_date_support_falls_back_and_warns(monkeypatch):
    ctrl = DashboardController()
    original = ctrl.mes.register_order

    def no_dates(*args, **kwargs):
        if "fecha_entrega" in kwargs:
            raise TypeError("unexpected keyword argument 'fecha_entrega'")
        return original(*args, **kwargs)

    monkeypatch.setattr(ctrl.mes, "register_order", no_dates)
    assert ctrl.act("register", product="P", quantity=3, due="2026-12-01")["ok"] is True
    assert len(ctrl.state()["orders"]) == 1
    assert any(e["kind"] == "log" and e["level"] == "WARNING" for e in ctrl.trace.entries)


def test_dispatch_runs_the_order_chosen_by_the_policy_through_a_command():
    ctrl = DashboardController()
    register(ctrl, 40)
    small = register(ctrl, 5)
    ctrl.act("strategy", key="smallest")
    result = ctrl.act("dispatch")
    assert result["ok"] is True and result["order_id"] == small
    statuses = {o["id"]: o["status"] for o in ctrl.state()["orders"]}
    assert statuses[small] == "En producción"
    assert small not in queue_ids(ctrl)
    history = ctrl.state()["commands"]
    assert history[0]["estado"] == "EJECUTADO" and small in history[0]["comando"]
    assert any(e["kind"] == "command" and small in e["text"] for e in ctrl.trace.entries)


def test_dispatch_without_pending_orders_reports_an_error():
    result = DashboardController().act("dispatch")
    assert result["ok"] is False and "pendientes" in result["error"]


def test_failed_command_is_listed_as_fallido_and_the_error_is_returned():
    ctrl = DashboardController()
    result = ctrl.act("run", order_id="NO-EXISTE")
    assert result["ok"] is False
    assert ctrl.state()["commands"][0]["estado"] == "FALLIDO"
    assert any(e["kind"] == "command" and e["state"] == "FALLIDO" for e in ctrl.trace.entries)


def test_undo_reverts_starting_the_cell_and_a_second_undo_is_refused():
    ctrl = DashboardController()
    ctrl.act("start_cell")
    assert ctrl.state()["cell"]["operating"] is True
    assert ctrl.act("undo")["ok"] is True
    assert ctrl.state()["cell"]["operating"] is False
    assert ctrl.state()["commands"][0]["estado"] == "DESHECHO"
    assert ctrl.act("undo")["ok"] is False


def test_undo_is_refused_when_orders_are_in_production():
    ctrl = DashboardController()
    ctrl.act("start_cell")
    order_id = register(ctrl, 5)
    ctrl.act("run", order_id=order_id)
    result = ctrl.act("undo")
    assert result["ok"] is False
    assert ctrl.state()["cell"]["operating"] is True
