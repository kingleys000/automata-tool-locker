import pytest
from app.web import create_app


@pytest.fixture
def app(tmp_path, config, clock):
    app = create_app(config, database=tmp_path / "web.sqlite", clock=clock, root=tmp_path)
    app.config["TESTING"] = True
    yield app
    app.extensions["engine"].close()


def headers(app):
    return {"X-Control-Token": app.extensions["control_token"], "Origin": "http://localhost"}


@pytest.mark.parametrize("address", ["192.168.1.20", "10.0.0.10", "::ffff:192.168.1.4"])
def test_tablet_read_only_even_with_token_and_forwarded_header(app, address):
    client = app.test_client()
    remote = {"REMOTE_ADDR": address}
    assert client.get("/monitor", environ_overrides=remote).status_code == 200
    assert client.get("/api/estado", environ_overrides=remote).status_code == 200
    assert client.get("/control", environ_overrides=remote).status_code == 403
    result = client.post("/api/acciones", json={"id":"x", "action":"presencia", "payload":{"value":True}},
                         headers={**headers(app), "X-Forwarded-For":"127.0.0.1"}, environ_overrides=remote)
    assert result.status_code == 403
    assert not app.extensions["engine"].state["presence"]


def test_local_token_and_same_origin_required(app):
    client = app.test_client()
    payload = {"id":"x", "action":"presencia", "payload":{"value":True}}
    assert client.post("/api/acciones", json=payload).status_code == 403
    assert client.post("/api/acciones", json=payload, headers={**headers(app), "Origin":"https://other.test"}).status_code == 403
    assert client.post("/api/acciones", json=payload, headers=headers(app)).status_code == 200
    assert app.extensions["engine"].state["presence"]


def test_monitor_has_no_controls_or_token(app):
    response = app.test_client().get("/monitor")
    html = response.get_data(as_text=True)
    assert "data-action=" not in html
    assert app.extensions["control_token"] not in html
    assert 'id="graph-inventario"' in html and 'id="graph-operacion"' in html
    assert "Puerta y sensores simulados" in html


def test_control_uses_camera_configuration_and_current_session(tmp_path, config):
    config.update(camera_source=3, roi=[.1, .2, .6, .7])
    app = create_app(config, root=tmp_path)
    try:
        client = app.test_client()
        html = client.get("/control").get_data(as_text=True)
        assert '<option value="3" selected>' in html
        assert 'id="roi-x" type="number" min="0" max="1" step=".05" value="0.1"' in html
        assert 'id="roi-h" type="number" min=".05" max="1" step=".05" value="0.7"' in html
        # Recargar conserva también los valores elegidos durante esta ejecución.
        camera = app.extensions["camera"]
        camera.source, camera.roi = 2, [.0, .0, .5, .5]
        html = client.get("/control").get_data(as_text=True)
        assert '<option value="2" selected>' in html
        assert 'id="roi-h" type="number" min=".05" max="1" step=".05" value="0.5"' in html
    finally:
        app.extensions["engine"].close()


def test_rebinding_host_cannot_read_control_token(app):
    assert app.test_client().get("/control", headers={"Host":"evil.example"}).status_code == 403


def test_history_cursor_reconnect_and_csv(app):
    client = app.test_client()
    before = client.get("/api/estado").get_json()
    client.post("/api/acciones", json={"id":"a", "action":"presencia", "payload":{"value":True}}, headers=headers(app))
    after = client.get("/api/estado?desde="+str(before["cursor"])).get_json()
    assert all(event["seq"] > before["cursor"] for event in after["events"])
    assert after["state"]["presence"]
    empty = client.get("/api/estado?desde="+str(after["cursor"])).get_json()
    assert not empty["events"]
    assert client.get("/api/historial.csv").status_code == 200
    assert "simulador" in client.get("/api/historial.csv").get_data(as_text=True)
    assert client.get("/api/estado?desde=-1").status_code == 400
    assert client.get("/api/estado?desde=no").status_code == 400


def test_bad_payload_and_fake_observation_endpoint(app):
    client = app.test_client()
    assert client.post("/api/acciones", json=[], headers=headers(app)).status_code == 400
    response = client.post("/api/acciones", json={"id":"fake", "action":"observe", "payload":{"label":"martillo"}}, headers=headers(app))
    assert response.status_code == 409
    assert not app.extensions["engine"].snapshot()["camera"]["fresh"]
    assert client.get("/api/camara/imagen").status_code == 503


def test_invalid_camera_configuration_and_capture_without_video(app):
    client = app.test_client()
    for i, (name, payload) in enumerate([
        ("camara_iniciar", {"source":"https://invalid"}),
        ("camara_iniciar", {"source":0,"roi":[.9,.9,.5,.5]}),
        ("capturar", {"label":"martillo","split":"train","session":"session1"}),
        ("capturar", {"label":"martillo","split":"train","session":"../../escape"}),
    ]):
        response = client.post("/api/acciones", json={"id":str(i),"action":name,"payload":payload}, headers=headers(app))
        assert response.status_code == 409
