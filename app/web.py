import atexit
import csv
import hmac
import io
import ipaddress
import json
from pathlib import Path
import secrets
import socket
import threading
from urllib.parse import urlsplit

from flask import Flask, Response, jsonify, render_template, request

from .camera import CameraManager
from .engine import Engine

ROOT = Path(__file__).resolve().parent.parent


def is_loopback(address):
    try:
        ip = ipaddress.ip_address(address or "")
        return ip.is_loopback or bool(getattr(ip, "ipv4_mapped", None) and ip.ipv4_mapped.is_loopback)
    except ValueError:
        return False


def create_app(config=None, database=None, clock=None, start_worker=False, root=None):
    root = Path(root or ROOT)
    settings = json.loads((ROOT / "config.json").read_text("utf-8"))
    settings.update(config or {})
    flask_app = Flask(__name__, template_folder=str(ROOT / "templates"), static_folder=str(ROOT / "static"))
    flask_app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
    engine = Engine(database or root / "data" / "prestamos.sqlite", settings, **({"clock": clock} if clock else {}))
    camera = CameraManager(engine, root, settings)
    token = secrets.token_urlsafe(32)
    stop = threading.Event()
    flask_app.extensions.update(engine=engine, camera=camera, worker_stop=stop, control_token=token)

    @flask_app.before_request
    def local_control_only():
        # No se confía en X-Forwarded-For; no hay proxy en esta arquitectura.
        if request.path == "/control" or (request.method not in ("GET", "HEAD", "OPTIONS")):
            if not is_loopback(request.remote_addr):
                return jsonify(ok=False, message="La tablet tiene acceso de solo lectura. Usa el control local del computador."), 403
            host = urlsplit(request.host_url).hostname
            if host not in ("127.0.0.1", "localhost", "::1"):
                return jsonify(ok=False, message="Abre el control usando http://127.0.0.1:8000/control."), 403
        if request.method not in ("GET", "HEAD", "OPTIONS"):
            supplied = request.headers.get("X-Control-Token", "")
            if not supplied.isascii() or not hmac.compare_digest(supplied, token):
                return jsonify(ok=False, message="Sesión de control vencida. Recarga la página."), 403
            origin = request.headers.get("Origin")
            if origin and origin != request.host_url.rstrip("/"):
                return jsonify(ok=False, message="Origen de la acción no permitido."), 403
            if request.headers.get("Sec-Fetch-Site") == "cross-site":
                return jsonify(ok=False, message="Acción desde otro sitio rechazada."), 403

    @flask_app.after_request
    def headers(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
        return response

    @flask_app.get("/")
    @flask_app.get("/monitor")
    def monitor():
        return render_template("portal.html", mode="monitor", token="")

    @flask_app.get("/control")
    def control():
        return render_template("portal.html", mode="control", token=token, camera=camera.info())

    @flask_app.get("/api/estado")
    def state():
        try:
            since = int(request.args.get("desde", 0))
            if since < 0 or since > 2 ** 63 - 1:
                raise ValueError
        except ValueError:
            return jsonify(ok=False, message="El cursor debe ser un entero no negativo."), 400
        data = engine.snapshot(since)
        data["camera_device"] = camera.info()
        return jsonify(data)

    @flask_app.post("/api/acciones")
    def action():
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or not isinstance(data.get("action"), str) or not isinstance(data.get("payload", {}), dict):
            return jsonify(ok=False, message="Envía action, payload e id en un objeto JSON."), 400
        action_id = data.get("id")
        if not isinstance(action_id, str) or not 1 <= len(action_id) <= 100:
            return jsonify(ok=False, message="Falta un identificador de acción válido."), 400
        name, payload = data["action"], data.get("payload", {})
        if name in ("camara_iniciar", "camara_detener", "capturar"):
            try:
                if name == "camara_iniciar":
                    message = camera.start(payload.get("source"), payload.get("roi"))
                elif name == "camara_detener":
                    message = camera.stop()
                else:
                    message = camera.capture(payload.get("label"), payload.get("split"), payload.get("session"))
                return jsonify(ok=True, message=message)
            except ValueError as exc:
                return jsonify(ok=False, message=str(exc)), 409
        result = engine.dispatch(name, payload, action_id)
        return jsonify(result), 200 if result["ok"] else 409

    @flask_app.get("/api/camara/imagen")
    def image():
        jpeg = camera.image()
        if jpeg is None:
            return jsonify(ok=False, message="No hay una imagen reciente."), 503
        return Response(jpeg, mimetype="image/jpeg")

    @flask_app.get("/api/historial.csv")
    def history():
        output = io.StringIO(newline="")
        writer = csv.writer(output)
        columns = ["seq", "time", "machine", "event", "previous", "current", "source", "accepted", "message"]
        writer.writerow(columns)
        with engine.lock:
            for row in engine.db.execute("SELECT * FROM events ORDER BY seq"):
                writer.writerow([row[c] for c in columns])
        return Response("\ufeff" + output.getvalue(), mimetype="text/csv; charset=utf-8",
                        headers={"Content-Disposition": "attachment; filename=historial.csv"})

    @flask_app.get("/api/conexion")
    def connection():
        try:
            addresses = {info[4][0] for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)}
        except OSError:
            addresses = set()
        addresses = sorted(ip for ip in addresses if not is_loopback(ip))
        return jsonify(urls=[f"http://{ip}:{settings['port']}/monitor" for ip in addresses], port=settings["port"])

    def ticker():
        while not stop.wait(.25):
            engine.tick()

    if start_worker:
        threading.Thread(target=ticker, daemon=True, name="verification-watchdog").start()
        atexit.register(stop.set)
        atexit.register(camera.stop)
    return flask_app

