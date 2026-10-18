"""Servidor aislado SOLO para prueba de UI. No utiliza ni entrena la cámara real.

La fuente de observaciones controladas existe únicamente en este test, sin
endpoint para falsificar reconocimiento en la aplicación entregada.
"""
from pathlib import Path
import sys
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.web import create_app
from waitress import serve


if __name__ == "__main__":
    (ROOT / "artifacts").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ui_test_", dir=ROOT / "artifacts") as folder:
        assert Path(folder).resolve().is_relative_to((ROOT / "artifacts").resolve())
        app = create_app({"port": 8101}, root=folder, start_worker=True)
        engine = app.extensions["engine"]

        def controlled_observations():
            frame_id = 0
            while True:
                with engine.lock:
                    label = "martillo" if engine.state["presence"] else "vacio"
                frame_id += 1
                engine.observe(label, .97, frame_id, time.monotonic())
                time.sleep(.1)

        threading.Thread(target=controlled_observations, daemon=True).start()
        print("UI_FIXTURE_READY", flush=True)
        serve(app, host="127.0.0.1", port=8101, threads=6)
