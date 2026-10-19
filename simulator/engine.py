"""Estado compartido del simulador. Solo utiliza las tablas de los autómatas."""
from collections import OrderedDict, deque
from copy import deepcopy
import json
import threading
import time

from app.automata import DEFINITIONS, transition


SCENARIOS = {
    "ciclo": {"name": "Ciclo completo", "description": "Reserva, retiro, devolución y aprobación."},
    "incorrecta": {"name": "Objeto incorrecto", "description": "Una devolución rechazada y su corrección."},
    "fallo": {"name": "Fallo y recuperación", "description": "Desconexión del sensor durante la verificación."},
    "dano": {"name": "Daño y reparación", "description": "Revisión, fuera de servicio y nueva aprobación."},
    "cancelacion": {"name": "Cancelar reserva", "description": "La herramienta permanece dentro; no se crea préstamo."},
}
LABELS = {
    "solicitar": "Solicitar martillo", "abrir": "Abrir puerta", "retirar": "Retirar martillo",
    "cerrar": "Ordenar cierre", "confirmar_cierre": "Confirmar puerta cerrada",
    "verificar": "Verificar contenido", "finalizar": "Finalizar operación",
    "devolver": "Iniciar devolución", "depositar": "Depositar objeto", "aprobar": "Aprobar herramienta",
    "cancelar": "Cancelar reserva", "desconectar": "Desconectar sensor", "conectar": "Reconectar sensor",
    "reintentar": "Reintentar operación", "danada": "Registrar daño", "reparada": "Registrar reparación",
}


def script_for(name):
    borrow = [(action, {}) for action in ("solicitar", "abrir", "retirar", "cerrar", "confirmar_cierre", "verificar", "finalizar")]
    returning = [("devolver", {}), ("abrir", {})]
    if name == "cancelacion":
        return [(action, {}) for action in ("solicitar", "abrir", "cancelar", "confirmar_cierre", "verificar", "finalizar")]
    if name == "incorrecta":
        returning += [("depositar", {"object": "alicate"}), ("cerrar", {})]
    returning += [("depositar", {"object": "martillo"}), ("cerrar", {}), ("confirmar_cierre", {})]
    if name == "fallo":
        returning += [(action, {}) for action in ("desconectar", "conectar", "reintentar", "abrir", "cerrar", "confirmar_cierre")]
    returning += [("verificar", {}), ("finalizar", {})]
    review = [("danada", {}), ("reparada", {}), ("aprobar", {})] if name == "dano" else [("aprobar", {})]
    return borrow + returning + review


class Simulation:
    def __init__(self, clock=time.monotonic):
        self.clock = clock
        self.lock = threading.RLock()
        self.events = deque(maxlen=200)
        self.requests = OrderedDict()
        self.revision = 0
        self.last_transitions = {}
        self.speed = 1.8
        self.demo = None
        self._reset()

    def _event(self, event, message, machine=None, previous=None, current=None, accepted=True):
        self.revision += 1
        row = dict(seq=self.revision, event=event, message=message, machine=machine,
                   previous=previous, current=current, accepted=accepted)
        self.events.append(row)
        self.state["message"] = message
        if machine:
            self.last_transitions[machine] = row

    def _reset(self):
        self.state = dict(inventory="Disponible", operation="Inactiva", mode=None,
                          object="martillo", door_closed=True, sensor_connected=True,
                          loan_active=False, loan_count=0, returned_count=0,
                          message="El martillo está disponible. Inicia un préstamo o una demostración.")
        self.events.clear()
        self.last_transitions.clear()
        self.demo = None
        self._event("reinicio", self.state["message"])

    def _move(self, machine, event, message):
        key = "inventory" if machine == "inventario" else "operation"
        previous = self.state[key]
        current = transition(machine, previous, event)
        self.state[key] = current
        self._event(event, message, machine, previous, current)

    @staticmethod
    def _require(condition, message):
        if not condition:
            raise ValueError(message)

    def _content_matches(self):
        expected = "vacio" if self.state["mode"] == "prestamo" else "martillo"
        self._require(self.state["object"] == expected,
                      "El compartimiento debe estar vacío para retirar." if expected == "vacio" else
                      "Se esperaba un martillo. Corrige el objeto antes de continuar.")

    def _apply(self, action, payload):
        s = self.state
        if action in ("solicitar", "devolver"):
            self._require(s["operation"] == "Inactiva", "Termina la operación actual antes de iniciar otra.")
            self._require(s["sensor_connected"] and s["door_closed"], "Se requiere sensor conectado y puerta cerrada.")
            if action == "solicitar":
                self._require(s["inventory"] == "Disponible" and s["object"] == "martillo", "El martillo debe estar disponible y dentro del compartimiento.")
                self._move("inventario", "solicitud_verificada", "Solicitud aceptada: el martillo queda reservado.")
                s["mode"] = "prestamo"
            else:
                self._require(s["inventory"] == "Prestada" and s["loan_active"], "No existe un préstamo activo para devolver.")
                self._require(s["object"] == "vacio", "El compartimiento debe estar vacío al iniciar la devolución.")
                s["mode"] = "devolucion"
            self._move("operacion", "iniciar", "Orden de apertura enviada a la puerta virtual.")
        elif action == "abrir":
            self._require(s["operation"] == "Abriendo" and s["sensor_connected"], "No hay una apertura pendiente con sensor conectado.")
            s["door_closed"] = False
            self._move("operacion", "abrir_deposito" if s["mode"] == "devolucion" else "abrir_retiro", "La puerta está abierta. Puedes interactuar con la herramienta.")
        elif action in ("retirar", "depositar"):
            self._require(not s["door_closed"] and s["operation"] in ("Esperando retiro", "Esperando depósito"), "Abre la puerta y espera la fase de retiro o depósito.")
            obj = "vacio" if action == "retirar" else payload.get("object", "martillo")
            if action == "depositar":
                self._require(obj in ("martillo", "alicate", "destornillador"), "Selecciona un objeto válido.")
            s["object"] = obj
            self._event(action, "Objeto retirado del compartimiento." if obj == "vacio" else f"Objeto depositado: {obj}.")
        elif action in ("cerrar", "cancelar"):
            self._require(s["operation"] in ("Esperando retiro", "Esperando depósito") and s["sensor_connected"], "La operación debe estar esperando retiro o depósito, con el sensor conectado.")
            if action == "cancelar":
                self._require(s["mode"] in ("prestamo", "cancelacion") and s["object"] == "martillo", "Para cancelar la reserva, deja el martillo dentro.")
                s["mode"] = "cancelacion"
            else:
                self._content_matches()
            self._move("operacion", "solicitar_cierre", "Cierre en curso. Falta la confirmación de la puerta.")
        elif action == "confirmar_cierre":
            self._require(s["operation"] == "Cerrando" and s["sensor_connected"], "No hay un cierre pendiente con sensor conectado.")
            s["door_closed"] = True
            self._move("operacion", "cierre_confirmado", "Puerta cerrada. Se comprueba el contenido virtual.")
        elif action == "verificar":
            self._require(s["operation"] == "Verificando" and s["sensor_connected"] and s["door_closed"], "La verificación requiere puerta cerrada y sensor conectado.")
            self._content_matches()
            if s["mode"] == "prestamo":
                s["loan_active"] = True
                s["loan_count"] += 1
                event = "retiro_verificado"
            elif s["mode"] == "devolucion":
                self._require(s["loan_active"], "No existe un préstamo activo.")
                s["loan_active"] = False
                s["returned_count"] += 1
                event = "devolucion_verificada"
            else:
                event = "cancelacion_verificada"
            self._move("inventario", event, "Contenido virtual correcto: se actualiza el inventario.")
            self._move("operacion", "verificacion_correcta", "Verificación simulada completa. Finaliza la operación.")
        elif action == "finalizar":
            self._move("operacion", "finalizar", "Operación terminada. El inventario conserva su estado.")
            s["mode"] = None
        elif action in ("desconectar", "conectar"):
            s["sensor_connected"] = action == "conectar"
            self._event(action, "Sensor virtual reconectado." if s["sensor_connected"] else "Sensor virtual desconectado.")
            if action == "desconectar" and s["operation"] not in ("Inactiva", "Completada", "Incidencia"):
                self._move("operacion", "fallo", "Incidencia: la operación se detiene hasta recuperar el sensor.")
        elif action == "reintentar":
            self._require(s["operation"] == "Incidencia" and s["sensor_connected"], "Reconecta el sensor antes de reintentar una incidencia.")
            event = "reabrir" if s["door_closed"] else "recuperar_deposito" if s["mode"] == "devolucion" else "recuperar_retiro"
            self._move("operacion", event, "Operación recuperada. Revisa el contenido y continúa.")
        elif action in ("aprobar", "danada", "reparada"):
            self._require(s["operation"] == "Inactiva", "Finaliza la operación antes de revisar la herramienta.")
            if action == "aprobar":
                self._require(s["object"] == "martillo" and s["door_closed"] and s["sensor_connected"], "La aprobación requiere el martillo dentro, puerta cerrada y sensor conectado.")
            event = {"aprobar": "aprobacion", "danada": "dano", "reparada": "reparacion"}[action]
            self._move("inventario", event, {"aprobar": "Martillo aprobado y disponible nuevamente.", "danada": "Daño registrado: herramienta fuera de servicio.", "reparada": "Reparación registrada: requiere otra revisión."}[action])
        else:
            raise ValueError("Acción de simulación desconocida.")

    def _attempt(self, action, payload):
        before = deepcopy(self.state)
        try:
            self._apply(action, payload)
            return {"ok": True, "message": self.state["message"]}
        except ValueError as exc:
            self.state = before
            message = str(exc)
            self._event(action, message, accepted=False)
            return {"ok": False, "message": message}

    def _next(self):
        s = self.state
        if not s["sensor_connected"]:
            return "conectar", {}
        op = s["operation"]
        if op == "Inactiva":
            return {"Disponible": ("solicitar", {}), "Prestada": ("devolver", {}),
                    "En revisión": ("aprobar", {}), "Fuera de servicio": ("reparada", {})}.get(s["inventory"], (None, {}))
        if op == "Esperando retiro":
            return ("retirar", {}) if s["mode"] == "prestamo" and s["object"] != "vacio" else ("cerrar", {})
        if op == "Esperando depósito":
            return ("depositar", {"object": "martillo"}) if s["object"] != "martillo" else ("cerrar", {})
        return ({"Abriendo": "abrir", "Cerrando": "confirmar_cierre", "Verificando": "verificar",
                 "Completada": "finalizar", "Incidencia": "reintentar"}.get(op), {})

    def _demo_step(self):
        demo = self.demo
        if not demo or demo["index"] >= len(demo["steps"]):
            return
        action, payload = demo["steps"][demo["index"]]
        self._attempt(action, payload)
        demo["index"] += 1
        if demo["index"] == len(demo["steps"]):
            demo["status"] = "finished"
            self._event("demostracion_completa", "Demostración terminada. Puedes reiniciar o explorar manualmente.")
        demo["next_at"] = self.clock() + self.speed

    def tick(self):
        with self.lock:
            if self.demo and self.demo["status"] == "playing" and self.clock() >= self.demo["next_at"]:
                self._demo_step()

    def dispatch(self, action, payload, request_id):
        with self.lock:
            encoded = json.dumps([action, payload], sort_keys=True)
            if request_id in self.requests:
                prior, result = self.requests[request_id]
                return deepcopy(result) if prior == encoded else {"ok": False, "message": "Identificador usado para otra acción."}
            try:
                if action == "reiniciar":
                    self._reset()
                elif action == "demostrar":
                    name = payload.get("scenario", "ciclo")
                    self._require(isinstance(name, str) and name in SCENARIOS, "Selecciona un escenario válido.")
                    self._reset()
                    self.demo = dict(scenario=name, steps=script_for(name), index=0, status="playing", next_at=self.clock() + .4)
                    self._event("demostracion", "Comienza la demostración: " + SCENARIOS[name]["name"] + ".")
                elif action == "pausar":
                    self._require(self.demo and self.demo["status"] == "playing", "No hay reproducción en curso.")
                    self.demo["status"] = "paused"
                elif action == "continuar":
                    self._require(self.demo and self.demo["status"] == "paused", "No hay una demostración pausada.")
                    self.demo.update(status="playing", next_at=self.clock() + self.speed)
                elif action == "velocidad":
                    value = payload.get("seconds")
                    self._require(type(value) in (int, float) and value in (.8, 1.8, 3.0), "Velocidad inválida.")
                    self.speed = value
                    if self.demo:
                        self.demo["next_at"] = self.clock() + value
                else:
                    self._require(not self.demo or self.demo["status"] != "playing", "Pausa la demostración para avanzar manualmente.")
                    if action == "paso" and self.demo and self.demo["status"] == "paused":
                        self._demo_step()
                    else:
                        self._require(not self.demo or self.demo["status"] != "paused", "Usa Siguiente paso para avanzar el escenario pausado, o reinicia para explorar libremente.")
                        if action == "paso":
                            action, payload = self._next()
                        result = self._attempt(action, payload)
                        self._remember(request_id, encoded, result)
                        return result
                result = {"ok": True, "message": self.state["message"]}
            except ValueError as exc:
                result = {"ok": False, "message": str(exc)}
            self._remember(request_id, encoded, result)
            return result

    def _remember(self, request_id, encoded, result):
        self.requests[request_id] = (encoded, result)
        if len(self.requests) > 1000:
            self.requests.popitem(last=False)

    def snapshot(self):
        with self.lock:
            action, payload = self._next()
            demo = None
            if self.demo:
                d = self.demo
                demo = dict(scenario=d["scenario"], status=d["status"], index=d["index"], total=len(d["steps"]))
                if d["status"] in ("playing", "paused") and d["index"] < len(d["steps"]):
                    action, payload = d["steps"][d["index"]]
            return deepcopy(dict(state=self.state, revision=self.revision, events=list(self.events),
                                 last_transitions=self.last_transitions, definitions=DEFINITIONS,
                                 scenarios=SCENARIOS, demo=demo, speed=self.speed,
                                 next_action=action, next_label=LABELS.get(action, "Siguiente paso")))
