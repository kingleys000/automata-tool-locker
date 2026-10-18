import json
import time
import pytest

from app.camera import CameraManager
from app.automata import CLASSES
from tools.train_model import inspect_dataset


def test_capture_uses_recent_frame_and_keeps_sessions_separate(engine, config, tmp_path):
    cv2 = pytest.importorskip("cv2")
    np = pytest.importorskip("numpy")
    camera = CameraManager(engine, tmp_path, config)
    # Imagen de prueba en memoria: verifica escritura, no reconocimiento real.
    camera.crop = np.zeros((40, 40, 3), dtype=np.uint8)
    camera.captured_at = time.monotonic()
    message = camera.capture("martillo", "train", "sesion_A")
    files = list((tmp_path / "dataset" / "train" / "martillo").glob("*.jpg"))
    assert len(files) == 1
    assert cv2.imread(str(files[0])).shape == (40, 40, 3)
    assert "sesion_A" in message
    assert json.loads((tmp_path / "dataset" / "sessions.json").read_text())["sesion_A"] == "train"
    with pytest.raises(ValueError, match="otro conjunto"):
        camera.capture("martillo", "test", "sesion_A")
    with pytest.raises(ValueError):
        camera.capture("martillo", "train", "../../escape")
    camera.captured_at = time.monotonic() - 10
    with pytest.raises(ValueError, match="reciente"):
        camera.capture("martillo", "train", "sesion_B")


def test_preview_never_returns_stale_image(engine, config, tmp_path):
    camera = CameraManager(engine, tmp_path, config)
    camera.jpeg = b"test-jpeg"
    camera.captured_at = time.monotonic() - 10
    assert camera.image() is None
    assert not camera.info()["preview_ready"]
    camera.captured_at = time.monotonic()
    assert camera.image() == b"test-jpeg"


def test_dataset_checker_rejects_missing_classes_and_session_leak(tmp_path):
    counts, errors = inspect_dataset(tmp_path)
    assert len(errors) == 15
    for split in ("train", "val", "test"):
        for label in CLASSES:
            target = tmp_path / split / label
            target.mkdir(parents=True)
            for i in range(10):
                # Solo comprueba estructura: no son fotografías ni datos de entrenamiento.
                (target / f"{split}_session__{i}.jpg").touch()
    counts, errors = inspect_dataset(tmp_path)
    assert not errors
    assert counts["train"]["martillo"] == 10
    (tmp_path / "test" / "martillo" / "train_session__100.jpg").touch()
    assert any("mezclada" in error for error in inspect_dataset(tmp_path)[1])


def test_capture_without_model_does_not_authorize_anything(engine, config, tmp_path):
    camera = CameraManager(engine, tmp_path, config)
    assert not camera.info()["model_ready"]
    assert not engine.dispatch("solicitar", {"code":"1001"}, "nomodel")["ok"]
    assert engine.state["inventory"] == "Disponible"
