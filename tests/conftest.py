import json
from pathlib import Path
import pytest

from app.engine import Engine


class Clock:
    def __init__(self):
        self.value = 100.0

    def __call__(self):
        return self.value

    def advance(self, seconds=.25):
        self.value += seconds
        return self.value


class Rig:
    def __init__(self, engine, clock):
        self.engine, self.clock = engine, clock
        self.number = 0
        self.frame = 0

    def act(self, action, code="1001", **payload):
        self.number += 1
        return self.engine.dispatch(action, {"code": code, **payload}, str(self.number))

    def ok(self, action, code="1001", **payload):
        result = self.act(action, code, **payload)
        assert result["ok"], result
        return result

    def stable(self, label, confidence=.96, count=10):
        for _ in range(count):
            self.frame += 1
            self.engine.observe(label, confidence, self.frame, self.clock.advance())

    def ready(self):
        self.ok("presencia", value=True)
        self.stable("martillo")

    def borrow(self):
        self.ready()
        self.ok("solicitar")
        self.ok("puerta_abierta")
        self.ok("presencia", value=False)
        self.stable("vacio")
        self.ok("cerrar")
        self.ok("puerta_cerrada")
        self.stable("vacio")
        assert self.engine.state["inventory"] == "Prestada"
        self.ok("finalizar")

    def returning(self):
        self.stable("vacio")
        self.ok("devolver")
        self.ok("puerta_abierta")

    def finish_return(self):
        self.ok("presencia", value=True)
        self.stable("martillo")
        self.ok("cerrar")
        self.ok("puerta_cerrada")
        self.stable("martillo")
        assert self.engine.state["inventory"] == "En revisión"
        self.ok("finalizar")


@pytest.fixture
def config():
    return json.loads((Path(__file__).resolve().parents[1] / "config.json").read_text("utf-8"))


@pytest.fixture
def clock():
    return Clock()


@pytest.fixture
def engine(tmp_path, config, clock):
    engine = Engine(tmp_path / "test.sqlite", config, clock=clock)
    yield engine
    engine.close()


@pytest.fixture
def rig(engine, clock):
    return Rig(engine, clock)
