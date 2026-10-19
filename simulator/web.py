"""Portal independiente: control local y autómatas de lectura para la tablet."""
import atexit
import hmac
import ipaddress
from pathlib import Path
import secrets
import socket
import threading
from urllib.parse import urlsplit

from flask import Flask, jsonify, redirect, render_template, request

from .engine import Simulation

ROOT = Path(__file__).resolve().parents[1]


def local(address):
    try:
        ip = ipaddress.ip_address(address or "")
        return ip.is_loopback or bool(getattr(ip, "ipv4_mapped", None) and ip.ipv4_mapped.is_loopback)
    except ValueError:
        return False


def create_simulator(port=8001, start_worker=False, clock=None):
    app = Flask(__name__, template_folder=str(ROOT / "templates"), static_folder=str(ROOT / "static"))
    app.config["MAX_CONTENT_LENGTH"] = 8192
    sim = Simulation(**({"clock": clock} if clock else {}))
    token = secrets.token_urlsafe(32)
    stop = threading.Event()
    app.extensions.update(simulation=sim, control_token=token, worker_stop=stop)

    @app.before_request
    def permissions():
        if request.path == "/simulador" or request.method not in ("GET", "HEAD", "OPTIONS"):
            if not local(request.remote_addr) or urlsplit(request.host_url).hostname not in ("localhost", "127.0.0.1", "::1"):
                return jsonify(ok=False, message="Abre /automatas en la tablet. El control se utiliza desde el computador."), 403
        if request.method not in ("GET", "HEAD", "OPTIONS"):
            supplied = request.headers.get("X-Simulation-Token", "")
            if not supplied.isascii() or not hmac.compare_digest(supplied, token):
                return jsonify(ok=False, message="Recarga el simulador para renovar la sesión."), 403
            if (request.headers.get("Origin") not in (None, request.host_url.rstrip("/"))
                    or request.headers.get("Sec-Fetch-Site") == "cross-site"):
                return jsonify(ok=False, message="Origen no permitido."), 403

    @app.after_request
    def headers(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
        return response

    @app.get("/")
    def index():
        return redirect("/simulador" if local(request.remote_addr) else "/automatas")

    @app.get("/simulador")
    def control():
        return render_template("simulation.html", mode="control", token=token)

    @app.get("/automatas")
    def automata():
        return render_template("simulation.html", mode="tablet", token="")

    @app.get("/api/simulacion/estado")
    def state():
        return jsonify(sim.snapshot())

    @app.post("/api/simulacion/acciones")
    def action():
        data = request.get_json(silent=True)
        if (not isinstance(data, dict) or not isinstance(data.get("action"), str)
                or not isinstance(data.get("payload", {}), dict)
                or not isinstance(data.get("id"), str) or not 1 <= len(data["id"]) <= 100):
            return jsonify(ok=False, message="Envía action, payload e id válidos."), 400
        result = sim.dispatch(data["action"], data.get("payload", {}), data["id"])
        return jsonify(result), 200 if result["ok"] else 409

    @app.get("/api/simulacion/conexion")
    def connection():
        try:
            addresses = sorted({info[4][0] for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET) if not local(info[4][0])})
        except OSError:
            addresses = []
        return jsonify(urls=[f"http://{ip}:{port}/automatas" for ip in addresses])

    if start_worker:
        def worker():
            while not stop.wait(.1):
                sim.tick()
        threading.Thread(target=worker, daemon=True, name="simulation-clock").start()
        atexit.register(stop.set)
    return app
