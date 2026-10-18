"""Definición compartida por el motor, los diagramas y el informe."""

INVENTORY = {
    "id": "inventario", "title": "Ciclo de la herramienta", "initial": "Disponible",
    "states": ["Disponible", "Reservada", "Prestada", "En revisión", "Fuera de servicio"],
    "transitions": [
        {"from": "Disponible", "event": "solicitud_verificada", "label": "Solicitud verificada", "to": "Reservada"},
        {"from": "Reservada", "event": "retiro_verificado", "label": "Retiro y cierre verificados", "to": "Prestada"},
        {"from": "Reservada", "event": "cancelacion_verificada", "label": "Cancelación verificada", "to": "Disponible"},
        {"from": "Prestada", "event": "devolucion_verificada", "label": "Devolución verificada", "to": "En revisión"},
        {"from": "En revisión", "event": "aprobacion", "label": "Aprobación", "to": "Disponible"},
        {"from": "En revisión", "event": "dano", "label": "Daño registrado", "to": "Fuera de servicio"},
        {"from": "Fuera de servicio", "event": "reparacion", "label": "Reparación terminada", "to": "En revisión"},
    ],
}

OPERATION = {
    "id": "operacion", "title": "Control de la operación", "initial": "Inactiva",
    "states": ["Inactiva", "Abriendo", "Esperando retiro", "Esperando depósito", "Cerrando", "Verificando", "Completada", "Incidencia"],
    "transitions": [
        {"from": "Inactiva", "event": "iniciar", "label": "Iniciar operación", "to": "Abriendo"},
        {"from": "Abriendo", "event": "abrir_retiro", "label": "Puerta abierta · préstamo", "to": "Esperando retiro"},
        {"from": "Abriendo", "event": "abrir_deposito", "label": "Puerta abierta · devolución", "to": "Esperando depósito"},
        {"from": "Esperando retiro", "event": "solicitar_cierre", "label": "Cerrar / cancelar", "to": "Cerrando"},
        {"from": "Esperando depósito", "event": "solicitar_cierre", "label": "Cerrar y verificar", "to": "Cerrando"},
        {"from": "Cerrando", "event": "cierre_confirmado", "label": "Sensor de cierre", "to": "Verificando"},
        {"from": "Verificando", "event": "verificacion_correcta", "label": "Nueva evidencia válida", "to": "Completada"},
        {"from": "Completada", "event": "finalizar", "label": "Finalizar", "to": "Inactiva"},
        *[{"from": state, "event": "fallo", "label": "Fallo / reinicio", "to": "Incidencia"}
          for state in ["Abriendo", "Esperando retiro", "Esperando depósito", "Cerrando", "Verificando"]],
        {"from": "Incidencia", "event": "reabrir", "label": "Reintentar · puerta cerrada", "to": "Abriendo"},
        {"from": "Incidencia", "event": "recuperar_retiro", "label": "Recuperar · puerta abierta", "to": "Esperando retiro"},
        {"from": "Incidencia", "event": "recuperar_deposito", "label": "Recuperar · puerta abierta", "to": "Esperando depósito"},
    ],
}
DEFINITIONS = {"inventario": INVENTORY, "operacion": OPERATION}
CLASSES = ("martillo", "destornillador", "alicate", "vacio", "otros")


def transition(machine, state, event):
    for edge in DEFINITIONS[machine]["transitions"]:
        if edge["from"] == state and edge["event"] == event:
            return edge["to"]
    raise ValueError(f"Evento {event!r} no permitido en {state!r}")


def recognize(events):
    """AFD académico: lenguaje de trazas válidas que terminan en Disponible.

    Una acción rechazada no se añade a una traza aceptada. Aquí cualquier
    símbolo inválido lleva al estado absorbente Error, también desde Error.
    """
    state = INVENTORY["initial"]
    trace = [state]
    for event in events:
        try:
            state = transition("inventario", state, event) if state != "Error" else "Error"
        except ValueError:
            state = "Error"
        trace.append(state)
    return {"accepted": state == "Disponible", "state": state, "trace": trace}
