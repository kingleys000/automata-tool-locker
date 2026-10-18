from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import pytest

from app.automata import DEFINITIONS, INVENTORY, recognize, transition
from app.engine import Engine
from conftest import Rig


def test_ten_complete_cycles(rig):
    for _ in range(10):
        rig.borrow()
        rig.returning()
        rig.finish_return()
        rig.ok("aprobar", code="ADMIN")
    snapshot = rig.engine.snapshot()
    assert snapshot["loan_count"] == 10
    assert all(loan["returned_at"] for loan in snapshot["loans"])
    assert snapshot["state"]["inventory"] == "Disponible"
    assert snapshot["state"]["operation"] == "Inactiva"
    events = []
    cursor = 0
    while True:
        page = rig.engine.snapshot(cursor, limit=11)
        events.extend(page["events"])
        cursor = page["cursor"]
        if not page["has_more"]:
            break
    assert len(events) == snapshot["revision"]
    assert len({event["seq"] for event in events}) == len(events)
    for event in events:
        if event["machine"]:
            assert transition(event["machine"], event["previous"], event["event"]) == event["current"]


@pytest.mark.parametrize("wrong", ["alicate", "destornillador", "otros", "vacio"])
def test_wrong_tool_never_closes_return(rig, wrong):
    rig.borrow()
    rig.returning()
    rig.ok("presencia", value=True)
    rig.stable(wrong)
    before = deepcopy(rig.engine.state)
    assert not rig.act("cerrar")["ok"]
    assert rig.engine.state == before
    assert rig.engine.snapshot()["active_loan"] is not None


def test_post_close_requires_new_frames(rig):
    rig.borrow()
    rig.returning()
    rig.ok("presencia", value=True)
    rig.stable("martillo")
    rig.ok("cerrar")
    rig.ok("puerta_cerrada")
    rig.engine.tick()
    assert rig.engine.state["operation"] == "Verificando"
    assert rig.engine.state["inventory"] == "Prestada"
    rig.stable("martillo", count=4)
    assert rig.engine.state["inventory"] == "Prestada"
    rig.stable("martillo")
    assert rig.engine.state["inventory"] == "En revisión"


def test_removing_object_after_close_fails_even_if_presence_lies(rig):
    rig.borrow()
    rig.returning()
    rig.ok("presencia", value=True)
    rig.stable("martillo")
    rig.ok("cerrar")
    rig.ok("puerta_cerrada")
    rig.stable("vacio")
    assert rig.engine.state["operation"] == "Incidencia"
    assert rig.engine.state["inventory"] == "Prestada"
    assert rig.engine.snapshot()["active_loan"]


def test_low_confidence_is_not_empty(rig):
    rig.ready()
    rig.ok("solicitar")
    rig.ok("puerta_abierta")
    rig.ok("presencia", value=False)
    rig.stable("vacio", confidence=.3)
    assert not rig.act("cerrar")["ok"]
    assert rig.engine.state["inventory"] == "Reservada"


def test_cancel_does_not_create_loan(rig):
    rig.ready()
    rig.ok("solicitar")
    rig.ok("puerta_abierta")
    rig.ok("cancelar")
    rig.ok("puerta_cerrada")
    rig.stable("martillo")
    rig.ok("finalizar")
    assert rig.engine.snapshot()["loan_count"] == 0
    assert rig.engine.state["inventory"] == "Disponible"


def test_authorization_and_duplicate_reservation(rig):
    rig.ready()
    assert not rig.act("solicitar", code="desconocido")["ok"]
    rig.ok("solicitar")
    assert not rig.act("solicitar", code="1002")["ok"]
    rig.ok("puerta_abierta")
    assert not rig.act("cancelar", code="1002")["ok"]


def test_only_borrower_can_return_and_only_admin_can_review(rig):
    rig.borrow()
    assert not rig.act("devolver", code="1002")["ok"]
    rig.returning()
    rig.finish_return()
    assert not rig.act("aprobar")["ok"]
    rig.ok("danada", code="ADMIN")
    assert rig.engine.state["inventory"] == "Fuera de servicio"
    assert not rig.act("solicitar")["ok"]
    rig.ok("reparada", code="ADMIN")
    assert rig.engine.state["inventory"] == "En revisión"
    rig.ok("aprobar", code="ADMIN")


@pytest.mark.parametrize("failure", ["camera", "sensor", "stale", "contradiction"])
def test_failure_during_final_check_is_recoverable(rig, failure):
    rig.borrow()
    rig.returning()
    rig.ok("presencia", value=True)
    rig.stable("martillo")
    rig.ok("cerrar")
    rig.ok("puerta_cerrada")
    if failure == "camera":
        rig.engine.camera_unavailable("Cámara desconectada")
    elif failure == "sensor":
        rig.ok("conexion_sensor", value=False)
    elif failure == "stale":
        rig.clock.advance(2)
        rig.engine.tick()
    else:
        rig.ok("presencia", value=False)
    assert rig.engine.state["operation"] == "Incidencia"
    assert rig.engine.state["inventory"] == "Prestada"
    assert rig.engine.snapshot()["active_loan"]
    rig.ok("conexion_sensor", value=True)
    rig.stable("martillo")
    rig.ok("reintentar")
    rig.ok("puerta_abierta")
    rig.finish_return()
    assert rig.engine.snapshot()["loan_count"] == 1


def test_repeated_old_future_or_invalid_observations_not_evidence(rig):
    e = rig.engine
    assert e.observe("martillo", .99, 1, rig.clock())
    assert not e.observe("martillo", .99, 1, rig.clock.advance())
    assert not e.observe("martillo", .99, 2, rig.clock() - 3)
    assert not e.observe("martillo", .99, 2, rig.clock() + 3)
    assert not e.observe("martillo", float("nan"), 2, rig.clock())
    assert not e.observe("martillo", 1.2, 2, rig.clock())
    assert not e.observe("inventada", .99, 2, rig.clock())
    assert not e.evidence("martillo")


def test_gaps_and_stale_evidence_cannot_authorize(rig):
    rig.ready()
    rig.clock.advance(3)
    assert not rig.act("solicitar")["ok"]
    rig.stable("martillo", count=3)
    assert not rig.act("solicitar")["ok"]
    rig.stable("martillo")
    rig.ok("solicitar")


def test_idempotence_and_simultaneous_requests(rig):
    rig.ready()
    def dispatch(_):
        return rig.engine.dispatch("solicitar", {"code":"1001"}, "same-id")
    with ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(dispatch, range(6)))
    assert all(result["ok"] for result in results)
    events = rig.engine.snapshot()["events"]
    assert sum(event["event"] == "solicitud_verificada" for event in events) == 1
    assert not rig.engine.dispatch("cancelar", {"code":"1001"}, "same-id")["ok"]


def test_restart_does_not_complete_pending_return(tmp_path, config, clock):
    database = tmp_path / "restart.sqlite"
    first = Engine(database, config, clock)
    rig = Rig(first, clock)
    rig.borrow()
    rig.returning()
    rig.ok("presencia", value=True)
    rig.stable("martillo")
    rig.ok("cerrar")
    rig.ok("puerta_cerrada")
    before = first.snapshot()["revision"]
    first.close()
    second = Engine(database, config, clock)
    try:
        assert second.state["operation"] == "Incidencia"
        assert second.state["inventory"] == "Prestada"
        assert second.snapshot()["active_loan"]
        assert second.snapshot()["revision"] > before
        assert not second.dispatch("reintentar", {"code":"1001"}, "recover")["ok"]
        assert not second.evidence("martillo")
    finally:
        second.close()


def test_invalid_actions_preserve_both_states(rig):
    for action in ["puerta_abierta", "puerta_cerrada", "cerrar", "devolver", "finalizar", "reintentar", "set_state", "observe", "danada"]:
        before = deepcopy(rig.engine.state)
        assert not rig.act(action)["ok"]
        assert rig.engine.state == before


def test_uncertain_final_check_times_out(rig):
    rig.borrow()
    rig.returning()
    rig.ok("presencia", value=True)
    rig.stable("martillo")
    rig.ok("cerrar")
    rig.ok("puerta_cerrada")
    rig.stable("otros", confidence=.4, count=55)
    assert rig.engine.state["operation"] == "Incidencia"
    assert rig.engine.snapshot()["active_loan"]


def test_formal_recognizer_and_complete_transition_definition():
    valid = ["solicitud_verificada", "retiro_verificado", "devolucion_verificada", "aprobacion"]
    assert recognize(valid)["accepted"]
    assert recognize([])["accepted"]
    assert recognize(valid[:-1])["state"] == "En revisión"
    assert not recognize(valid[:-1])["accepted"]
    assert recognize(["retiro_verificado"] + valid)["trace"] == ["Disponible"] + ["Error"] * 5
    assert recognize(["solicitud_verificada", "cancelacion_verificada"])["accepted"]
    for machine, definition in DEFINITIONS.items():
        symbols = {edge["event"] for edge in definition["transitions"]}
        for state in definition["states"]:
            for symbol in symbols:
                matching = [edge for edge in definition["transitions"] if edge["from"] == state and edge["event"] == symbol]
                assert len(matching) <= 1
                if matching:
                    assert transition(machine, state, symbol) == matching[0]["to"]
                else:
                    with pytest.raises(ValueError):
                        transition(machine, state, symbol)
