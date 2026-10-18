"""Contrato sustituible por un adaptador serial Arduino en la segunda etapa."""
from typing import Protocol


class HardwareAdapter(Protocol):
    simulated: bool

    def request(self, command: str) -> None: ...


class SimulatedHardware:
    simulated = True

    def request(self, command: str) -> None:
        # La orden NO equivale a confirmar un sensor. La confirmación llega
        # mediante un evento separado emitido desde los controles del portal.
        if command not in {"abrir", "cerrar"}:
            raise ValueError("Orden física desconocida")
