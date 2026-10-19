from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy

import pytest

from app.automata import transition
from simulator.engine import SCENARIOS, Simulation
from simulator.web import create_simulator


def act(sim, action, **payload):
    return sim.dispatch(action, payload, str(len(sim.requests) + 1))


@pytest.mark.parametrize("scenario", list(SCENARIOS))
def test_all_demonstrations_follow_shared_automata(scenario, clock):
    sim = Simulation(clock)
    assert act(sim, "demostrar", scenario=scenario)["ok"]
    for _ in range(50):
        clock.advance(4)
        sim.tick()
        if sim.snapshot()["demo"]["status"] == "finished":
            break
    result = sim.snapshot()
    assert result["demo"]["status"] == "finished"
    assert result["state"]["inventory"] == "Disponible"
    assert result["state"]["operation"] == "Inactiva"
    assert result["state"]["object"] == "martillo"
    assert not result["state"]["loan_active"]
    expected_loans = 0 if scenario == "cancelacion" else 1
    assert result["state"]["loan_count"] == expected_loans
    assert result["state"]["returned_count"] == expected_loans
    rejected = [e for e in result["events"] if not e["accepted"]]
    assert len(rejected) == (1 if scenario == "incorrecta" else 0)
    for event in result["events"]:
        if event["machine"]:
            assert transition(event["machine"], event["previous"], event["event"]) == event["current"]
    if scenario == "fallo":
        assert any(e["current"] == "Incidencia" for e in result["events"])
    if scenario == "dano":
        assert any(e["current"] == "Fuera de servicio" for e in result["events"])


def test_manual_steps_complete_ten_cycles_without_camera():
    sim = Simulation()
    for cycle in range(10):
        for _ in range(15):
            assert act(sim, "paso")["ok"]
        s = sim.snapshot()["state"]
        assert s["inventory"] == "Disponible"
        assert s["operation"] == "Inactiva"
        assert s["loan_count"] == cycle + 1
        assert s["returned_count"] == cycle + 1


def test_pause_step_and_resume_use_server_clock(clock):
    sim = Simulation(clock)
    act(sim, "demostrar")
    act(sim, "pausar")
    clock.advance(100)
    sim.tick()
    assert sim.snapshot()["demo"]["index"] == 0
    assert act(sim, "paso")["ok"]
    assert sim.snapshot()["state"]["inventory"] == "Reservada"
    assert sim.snapshot()["demo"]["index"] == 1
    clock.advance(100)
    sim.tick()
    assert sim.snapshot()["demo"]["index"] == 1
    act(sim, "continuar")
    sim.tick()
    assert sim.snapshot()["demo"]["index"] == 1
    clock.advance(2)
    sim.tick()
    assert sim.snapshot()["demo"]["index"] == 2
    assert not act(sim, "paso")["ok"]


def test_rejection_does_not_change_domain_state_and_reset_is_isolated():
    first, second = Simulation(), Simulation()
    before = deepcopy(first.state)
    assert not act(first, "devolver")["ok"]
    assert {k:v for k,v in first.state.items() if k != "message"} == {k:v for k,v in before.items() if k != "message"}
    assert first.events[-1]["accepted"] is False
    act(first, "solicitar")
    assert second.state["inventory"] == "Disponible"
    seq = first.revision
    act(first, "reiniciar")
    assert first.state["inventory"] == "Disponible"
    assert first.revision > seq
    assert len(first.events) == 1


def test_simulation_requests_are_idempotent_under_concurrency():
    sim = Simulation()
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(lambda _: sim.dispatch("solicitar", {}, "same-id"), range(6)))
    assert all(r["ok"] for r in results)
    assert sum(e["event"] == "solicitud_verificada" for e in sim.events) == 1
    assert not sim.dispatch("reiniciar", {}, "same-id")["ok"]
    assert sim.state["inventory"] == "Reservada"


def test_tablet_only_receives_diagrams_and_cannot_control():
    app = create_simulator()
    client = app.test_client()
    remote = {"REMOTE_ADDR": "192.168.1.20"}
    html = client.get("/automatas", environ_overrides=remote).get_data(as_text=True)
    assert 'id="graph-inventario"' in html and 'id="graph-operacion"' in html
    assert 'id="scene"' not in html and 'id="manual-controls"' not in html
    assert app.extensions["control_token"] not in html
    assert client.get("/simulador", environ_overrides=remote).status_code == 403
    assert client.get("/", environ_overrides=remote).location == "/automatas"
    headers = {"X-Simulation-Token": app.extensions["control_token"], "Origin": "http://localhost"}
    data = {"id": "test", "action": "solicitar", "payload": {}}
    assert client.post("/api/simulacion/acciones", json=data, headers=headers, environ_overrides=remote).status_code == 403
    assert client.post("/api/simulacion/acciones", json=data).status_code == 403
    assert client.post("/api/simulacion/acciones", json=data, headers={**headers,"Origin":"https://other.test"}).status_code == 403
    assert client.get("/simulador", headers={"Host":"other.test"}).status_code == 403
    assert client.post("/api/simulacion/acciones", json=data, headers=headers).status_code == 200
    assert client.get("/api/simulacion/estado", environ_overrides=remote).get_json()["state"]["inventory"] == "Reservada"
    assert client.get("/api/camara/imagen").status_code == 404


def test_simulator_rejects_malformed_input():
    app = create_simulator()
    client = app.test_client()
    headers = {"X-Simulation-Token": app.extensions["control_token"]}
    for data in ([], {}, {"id":"x","action": [],"payload":{}}, {"id":"x","action":"paso","payload":[]}):
        assert client.post("/api/simulacion/acciones", json=data, headers=headers).status_code == 400
    for action, payload in (("demostrar",{"scenario":[]}), ("velocidad",{"seconds":True}), ("velocidad",{"seconds":-1})):
        assert client.post("/api/simulacion/acciones", json={"id":str(payload),"action":action,"payload":payload}, headers=headers).status_code == 409
