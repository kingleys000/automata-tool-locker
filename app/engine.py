"""Motor determinista: una sola autoridad, evidencia reciente y persistencia atómica."""
from collections import deque
from copy import deepcopy
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import sqlite3
import threading
import time

from .automata import CLASSES, DEFINITIONS, transition
from .hardware import SimulatedHardware


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


class Rejected(Exception):
    pass


class Engine:
    def __init__(self, database, config, clock=time.monotonic, hardware=None):
        self.config = config
        self.clock = clock
        self.lock = threading.RLock()
        self.hardware = hardware or SimulatedHardware()
        self.frames = deque(maxlen=200)
        self.camera = {"connected": False, "label": None, "confidence": 0.0,
                       "error": "Cámara sin iniciar", "frame_id": -1, "timestamp": None}
        self.last_stable = None
        self.verify_since = None
        if str(database) != ":memory:":
            Path(database).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(database), check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY CHECK(id=1), value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS users (code TEXT PRIMARY KEY, name TEXT NOT NULL, role TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS loans (id INTEGER PRIMARY KEY AUTOINCREMENT, user_code TEXT NOT NULL,
                tool TEXT NOT NULL, borrowed_at TEXT NOT NULL, returned_at TEXT, simulated_hardware INTEGER NOT NULL);
            CREATE UNIQUE INDEX IF NOT EXISTS one_active_loan ON loans(tool) WHERE returned_at IS NULL;
            CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY AUTOINCREMENT, time TEXT NOT NULL,
                machine TEXT, event TEXT NOT NULL, previous TEXT, current TEXT, source TEXT NOT NULL,
                accepted INTEGER NOT NULL, message TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS requests (id TEXT PRIMARY KEY, payload TEXT NOT NULL, result TEXT NOT NULL);
        """)
        with self.db:
            self.db.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", [
                ("1001", "Estudiante 1", "usuario"), ("1002", "Estudiante 2", "usuario"),
                ("ADMIN", "Encargado", "encargado")])
            row = self.db.execute("SELECT value FROM state WHERE id=1").fetchone()
            self.state = json.loads(row[0]) if row else {
                "inventory": "Disponible", "operation": "Inactiva", "mode": None, "owner": None,
                "door_closed": True, "presence": False, "hardware_connected": True,
                "message": "Coloca el martillo y configura la cámara. Los sensores son simulados.",
            }
            if not row:
                self._event("inicializacion", "sistema", "Prototipo iniciado; sensores y puerta simulados.")
            elif self.state["operation"] not in ("Inactiva", "Completada", "Incidencia"):
                self._incident("Reinicio con operación pendiente. Revisa la caja virtual y pulsa Reintentar.")
            self._save()

    def close(self):
        with self.lock:
            self.db.close()

    def _save(self):
        self.db.execute("INSERT OR REPLACE INTO state VALUES (1, ?)", (json.dumps(self.state),))

    def _event(self, event, source, message, machine=None, previous=None, current=None, accepted=True):
        cursor = self.db.execute("INSERT INTO events(time,machine,event,previous,current,source,accepted,message) VALUES (?,?,?,?,?,?,?,?)",
                                 (utc(), machine, event, previous, current, source, int(accepted), message))
        return cursor.lastrowid

    def _move(self, machine, event, source, message):
        key = "inventory" if machine == "inventario" else "operation"
        previous = self.state[key]
        current = transition(machine, previous, event)
        self.state[key] = current
        self.state["message"] = message
        self._event(event, source, message, machine, previous, current)

    def _incident(self, message):
        if self.state["operation"] not in ("Inactiva", "Completada", "Incidencia"):
            self._move("operacion", "fallo", "sistema", message)
        self.state["message"] = message
        self.verify_since = None

    def _require(self, condition, message):
        if not condition:
            raise Rejected(message)

    def _user(self, code, admin=False):
        row = self.db.execute("SELECT * FROM users WHERE code=?", (str(code),)).fetchone()
        self._require(row is not None, "Código de usuario no registrado.")
        if admin:
            self._require(row["role"] == "encargado", "Esta acción requiere el código del encargado.")
        return dict(row)

    def _owner(self, code):
        user = self._user(code)
        self._require(user["code"] == self.state["owner"] or user["role"] == "encargado",
                      "La operación pertenece a otro usuario.")
        return user

    def _fresh(self):
        stamp = self.camera["timestamp"]
        return self.camera["connected"] and stamp is not None and 0 <= self.clock() - stamp <= self.config["fresh_seconds"]

    def evidence(self, label, since=None):
        if not self._fresh():
            return False
        suffix = []
        for frame in reversed(self.frames):
            if frame["label"] != label or frame["confidence"] < self.config["confidence"]:
                break
            if since is not None and frame["timestamp"] <= since:
                break
            if suffix and suffix[-1]["timestamp"] - frame["timestamp"] > self.config["fresh_seconds"]:
                break
            suffix.append(frame)
        return (len(suffix) >= self.config["min_frames"] and
                suffix[0]["timestamp"] - suffix[-1]["timestamp"] >= self.config["stable_seconds"])

    def _vision(self, label):
        self._require(self.evidence(label), f"Falta evidencia reciente y estable de «{label}» durante dos segundos.")

    def _active_loan(self):
        return self.db.execute("SELECT * FROM loans WHERE tool='martillo' AND returned_at IS NULL").fetchone()

    def dispatch(self, action, payload, request_id):
        """Las acciones inválidas no mutan el estado; el rechazo sí se registra."""
        with self.lock:
            encoded = json.dumps({"action": action, "payload": payload}, sort_keys=True)
            prior = self.db.execute("SELECT * FROM requests WHERE id=?", (request_id,)).fetchone()
            if prior:
                if prior["payload"] != encoded:
                    return {"ok": False, "message": "Identificador ya usado para otra acción."}
                return json.loads(prior["result"])
            before = deepcopy(self.state)
            prior_verify = self.verify_since
            try:
                with self.db:
                    self._apply(action, payload)
                    self._save()
                    result = {"ok": True, "message": self.state["message"]}
                    self.db.execute("INSERT INTO requests VALUES (?, ?, ?)", (request_id, encoded, json.dumps(result)))
            except (Rejected, ValueError) as exc:
                self.state = before
                self.verify_since = prior_verify
                result = {"ok": False, "message": str(exc)}
                with self.db:
                    self._event(action, "simulador" if action in ("presencia", "puerta_abierta", "puerta_cerrada", "conexion_sensor") else "usuario",
                                str(exc), accepted=False)
                    self.db.execute("INSERT INTO requests VALUES (?, ?, ?)", (request_id, encoded, json.dumps(result)))
            except Exception:
                self.state = before
                self.verify_since = prior_verify
                raise
            return result

    def _apply(self, action, payload):
        s = self.state
        code = payload.get("code", "")
        if action in ("solicitar", "devolver"):
            user = self._user(code)
            self._require(s["operation"] == "Inactiva", "Finaliza o recupera la operación actual antes de iniciar otra.")
            self._require(s["hardware_connected"] and s["door_closed"], "Se requiere sensor conectado y puerta cerrada.")
            if action == "solicitar":
                self._require(s["inventory"] == "Disponible", "La herramienta no está disponible.")
                self._require(s["presence"], "El sensor simulado no indica presencia.")
                self._vision("martillo")
                self._move("inventario", "solicitud_verificada", "usuario", "Martillo reservado. Orden de apertura enviada al simulador.")
                s["mode"] = "prestamo"
            else:
                self._require(s["inventory"] == "Prestada", "No hay una herramienta prestada para devolver.")
                loan = self._active_loan()
                self._require(loan is not None and loan["user_code"] == user["code"], "Selecciona el préstamo de su responsable.")
                self._require(not s["presence"], "El compartimiento debe estar vacío antes de devolver.")
                self._vision("vacio")
                s["mode"] = "devolucion"
            s["owner"] = user["code"]
            self.hardware.request("abrir")
            self._move("operacion", "iniciar", "usuario", "Confirma la apertura con el sensor simulado.")
        elif action == "puerta_abierta":
            self._require(s["hardware_connected"] and s["operation"] == "Abriendo", "No hay una apertura pendiente.")
            s["door_closed"] = False
            event = "abrir_deposito" if s["mode"] == "devolucion" else "abrir_retiro"
            self._move("operacion", event, "simulador", "Puerta abierta simulada. Retira o deposita la herramienta real.")
        elif action == "presencia":
            value = payload.get("value")
            self._require(isinstance(value, bool), "La presencia debe ser un valor booleano.")
            self._require(s["hardware_connected"], "El sensor está desconectado.")
            s["presence"] = value
            s["message"] = "Sensor simulado: " + ("objeto presente." if value else "compartimiento vacío.")
            self._event("presencia", "simulador", s["message"])
            if s["operation"] == "Verificando" and value != (s["mode"] != "prestamo"):
                self._incident("Presencia contradictoria después del cierre. La operación sigue pendiente.")
        elif action in ("cerrar", "cancelar"):
            self._owner(code)
            self._require(s["operation"] in ("Esperando retiro", "Esperando depósito"), "La operación no está esperando retiro o depósito.")
            self._require(s["hardware_connected"] and not s["door_closed"], "La puerta debe estar abierta y el sensor conectado.")
            if action == "cancelar":
                self._require(s["mode"] in ("prestamo", "cancelacion"), "Solo puede cancelarse una reserva de préstamo.")
                self._require(s["presence"], "Para cancelar, devuelve el martillo a la zona observada.")
                self._vision("martillo")
                s["mode"] = "cancelacion"
            else:
                # Reintentar una cancelación permite decidir nuevamente entre retirar o devolver.
                if s["mode"] == "cancelacion":
                    s["mode"] = "prestamo"
                expected = "vacio" if s["mode"] == "prestamo" else "martillo"
                self._require(s["presence"] == (expected == "martillo"), "El sensor simulado contradice la operación solicitada.")
                self._vision(expected)
            self.hardware.request("cerrar")
            self._move("operacion", "solicitar_cierre", "usuario", "Orden de cierre enviada. Confirma el sensor de puerta.")
        elif action == "puerta_cerrada":
            self._require(s["hardware_connected"] and s["operation"] == "Cerrando", "No hay un cierre pendiente.")
            s["door_closed"] = True
            self.verify_since = self.clock()
            self._move("operacion", "cierre_confirmado", "simulador", "Puerta cerrada simulada. Esperando NUEVAS imágenes para verificar.")
        elif action == "conexion_sensor":
            value = payload.get("value")
            self._require(isinstance(value, bool), "La conexión debe ser un valor booleano.")
            s["hardware_connected"] = value
            self._event("conexion_sensor", "simulador", "Sensor conectado." if value else "Sensor desconectado.")
            if not value:
                self._incident("Sensor desconectado. No se confirmará la operación.")
            else:
                s["message"] = "Sensor reconectado. Revisa sus valores antes de reintentar."
        elif action == "reintentar":
            self._owner(code)
            self._require(s["operation"] == "Incidencia", "No hay incidencia pendiente.")
            self._require(s["hardware_connected"] and self._fresh(), "Reconecta cámara y sensores antes de reintentar.")
            self.verify_since = None
            if s["door_closed"]:
                self.hardware.request("abrir")
                event = "reabrir"
            else:
                event = "recuperar_deposito" if s["mode"] == "devolucion" else "recuperar_retiro"
            self._move("operacion", event, "usuario", "Operación recuperada. Corrige el contenido y vuelve a cerrar.")
        elif action == "finalizar":
            self._owner(code)
            self._require(s["operation"] == "Completada", "La operación aún no está completada.")
            self._move("operacion", "finalizar", "usuario", "Operación terminada. El registro permanece en el historial.")
            s["mode"] = s["owner"] = None
        elif action in ("aprobar", "danada", "reparada"):
            self._user(code, admin=True)
            self._require(s["operation"] == "Inactiva", "Finaliza la operación antes de la revisión del encargado.")
            if action == "aprobar":
                self._require(s["hardware_connected"] and s["door_closed"] and s["presence"], "Verifica presencia y cierre antes de aprobar.")
                self._vision("martillo")
            event = {"aprobar": "aprobacion", "danada": "dano", "reparada": "reparacion"}[action]
            self._move("inventario", event, "usuario", {"aprobar": "Herramienta aprobada por el encargado.", "danada": "Herramienta fuera de servicio por revisión humana.", "reparada": "Reparación registrada; requiere una nueva revisión."}[action])
        else:
            raise Rejected("Acción desconocida.")

    def observe(self, label, confidence, frame_id, timestamp):
        """Solo el adaptador real (o un doble de pruebas) llama este método.

        No existe un endpoint público para inyectar una clase reconocida.
        """
        with self.lock:
            if (label not in CLASSES or not math.isfinite(confidence) or not 0 <= confidence <= 1
                    or not math.isfinite(timestamp) or timestamp > self.clock()
                    or self.clock() - timestamp > self.config["fresh_seconds"]
                    or frame_id <= self.camera["frame_id"]
                    or (self.camera["timestamp"] is not None and timestamp <= self.camera["timestamp"])):
                return False
            self.camera.update(connected=True, label=label, confidence=confidence, error=None,
                               frame_id=frame_id, timestamp=timestamp)
            self.frames.append({"label": label, "confidence": confidence, "frame_id": frame_id, "timestamp": timestamp})
            stable = label if self.evidence(label) else None
            with self.db:
                if stable and stable != self.last_stable:
                    self._event("reconocimiento_estable", "camara", f"Reconocimiento real estable: {stable}.")
                self.last_stable = stable
                self._evaluate()
                self._save()
            return True

    def camera_unavailable(self, message):
        with self.lock, self.db:
            changed = self.camera["error"] != message or self.camera["connected"]
            self.camera.update(connected=False, error=message, label=None, confidence=0.0)
            self.frames.clear()
            self.last_stable = None
            if changed:
                self._event("camara_no_disponible", "camara", message, accepted=False)
            if self.state["operation"] not in ("Inactiva", "Completada"):
                self._incident(message + " La operación permanece pendiente.")
            else:
                self.state["message"] = message + ". Inicia o reconecta la cámara antes de operar."
            self._save()

    def _evaluate(self):
        s = self.state
        if s["operation"] != "Verificando":
            return
        expected = "vacio" if s["mode"] == "prestamo" else "martillo"
        if not s["door_closed"] or not s["hardware_connected"] or s["presence"] != (expected == "martillo"):
            self._incident("Los sensores contradicen la comprobación final.")
        elif self.evidence(expected, since=self.verify_since):
            if s["mode"] == "prestamo":
                self.db.execute("INSERT INTO loans(user_code,tool,borrowed_at,simulated_hardware) VALUES (?,?,?,?)",
                                (s["owner"], "martillo", utc(), int(self.hardware.simulated)))
                event = "retiro_verificado"
            elif s["mode"] == "devolucion":
                updated = self.db.execute("UPDATE loans SET returned_at=? WHERE tool='martillo' AND returned_at IS NULL AND user_code=?", (utc(), s["owner"]))
                if updated.rowcount != 1:
                    self._incident("No se encontró un único préstamo activo. Requiere revisión.")
                    return
                event = "devolucion_verificada"
            else:
                event = "cancelacion_verificada"
            self._move("inventario", event, "camara", "Verificación real correcta con cierre y presencia simulados.")
            self._move("operacion", "verificacion_correcta", "camara", "Operación comprobada. Pulsa Finalizar; la puerta y los sensores son simulados.")
            self.verify_since = None
        elif any(self.evidence(label, since=self.verify_since) for label in CLASSES if label != expected):
            self._incident(f"El contenido después del cierre no corresponde a «{expected}».")
        elif self.verify_since is not None and self.clock() - self.verify_since > self.config["verification_timeout"]:
            self._incident("Tiempo de verificación agotado. Imagen insuficiente o dudosa.")

    def tick(self):
        with self.lock, self.db:
            if self.camera["connected"] and not self._fresh():
                self.camera_unavailable("No llegan observaciones recientes de la cámara")
            self._evaluate()
            self._save()

    def snapshot(self, since=0, limit=200):
        with self.lock:
            events = [dict(row) for row in self.db.execute("SELECT * FROM events WHERE seq>? ORDER BY seq LIMIT ?", (since, limit))]
            revision = self.db.execute("SELECT COALESCE(MAX(seq),0) FROM events").fetchone()[0]
            cursor = events[-1]["seq"] if events else min(since, revision)
            active = self._active_loan()
            camera = {key: value for key, value in self.camera.items() if key != "timestamp"}
            camera["fresh"] = self._fresh()
            camera["age_ms"] = None if self.camera["timestamp"] is None else round((self.clock() - self.camera["timestamp"]) * 1000)
            stable = next((label for label in CLASSES if self.evidence(label)), None)
            camera["stable_label"] = stable
            s = deepcopy(self.state)
            led = "rojo_intermitente" if s["operation"] == "Incidencia" else (
                "verde" if s["operation"] not in ("Inactiva", "Completada") else
                "rojo" if s["inventory"] != "Disponible" else "apagado")
            last = {}
            for machine in DEFINITIONS:
                row = self.db.execute("SELECT * FROM events WHERE machine=? AND accepted=1 ORDER BY seq DESC LIMIT 1", (machine,)).fetchone()
                last[machine] = dict(row) if row else None
            return {"state": s, "camera": camera, "tool": {"id": "martillo", "name": "Martillo", "compartment": "01"},
                    "simulated_hardware": self.hardware.simulated, "led": led, "definitions": DEFINITIONS,
                    "events": events, "cursor": cursor, "has_more": cursor < revision, "revision": revision,
                    "last_transitions": last, "active_loan": dict(active) if active else None,
                    "loan_count": self.db.execute("SELECT COUNT(*) FROM loans").fetchone()[0],
                    "loans": [dict(row) for row in self.db.execute("SELECT * FROM loans ORDER BY id DESC LIMIT 20")],
                    "users": [dict(row) for row in self.db.execute("SELECT * FROM users ORDER BY code")],
                    "server_time": utc(), "threshold": self.config["confidence"]}
