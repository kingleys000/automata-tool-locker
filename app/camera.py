"""Una captura real compartida. Sin modelo, solo previsualización y dataset."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import threading
import time

from .automata import CLASSES


class CameraManager:
    def __init__(self, engine, root, config):
        self.engine, self.root, self.config = engine, Path(root), config
        self.lock = threading.RLock()
        self.thread = None
        self.inference_thread = None
        self.stop_event = threading.Event()
        self.jpeg = self.crop = None
        self.captured_at = None
        self.frame_id = 0
        self.status = "Sin iniciar"
        self.model_ready = False
        self.source = config["camera_source"]
        self.roi = config["roi"]

    def start(self, source=None, roi=None):
        with self.lock:
            if (self.thread and self.thread.is_alive()) or (self.inference_thread and self.inference_thread.is_alive()):
                raise ValueError("La cámara ya está activa. Deténla antes de cambiar su configuración.")
            if source is None:
                source = self.source
            if isinstance(source, bool) or not isinstance(source, int) or not 0 <= source <= 9:
                raise ValueError("Selecciona un índice de cámara entre 0 y 9 (DroidCam aparece como cámara de Windows).")
            roi = self.roi if roi is None else roi
            if not isinstance(roi, list) or len(roi) != 4 or not all(type(v) in (int, float) and 0 <= v <= 1 for v in roi):
                raise ValueError("ROI inválida: usa [x, y, ancho, alto] entre 0 y 1.")
            x, y, w, h = roi
            if w < .05 or h < .05 or x + w > 1.00001 or y + h > 1.00001:
                raise ValueError("El área observada debe caber en la imagen y medir al menos 5 % por lado.")
            self.source, self.roi = source, roi
            self.stop_event = threading.Event()
            self.status = "Conectando cámara…"
            self.model_ready = False
            self.jpeg = self.crop = self.captured_at = None
            self.thread = threading.Thread(target=self._run, args=(self.stop_event,), daemon=True, name="camera")
            self.thread.start()
            return "Cámara iniciándose. La carga del modelo puede tardar unos segundos."

    def stop(self):
        with self.lock:
            self.stop_event.set()
            self.jpeg = self.crop = self.captured_at = None
            self.model_ready = False
            self.status = "Cámara detenida"
            self.engine.camera_unavailable("Cámara detenida por el operador")
        if self.thread:
            self.thread.join(timeout=2)
        if self.inference_thread:
            self.inference_thread.join(timeout=2)
        return "Cámara detenida. No se conservará evidencia visual anterior."

    def info(self):
        with self.lock:
            fresh = self.captured_at is not None and time.monotonic() - self.captured_at <= self.config["fresh_seconds"]
            return {"running": bool(self.thread and self.thread.is_alive()), "status": self.status,
                    "model_ready": self.model_ready, "model_path": self.config["model_path"],
                    "preview_ready": fresh and self.jpeg is not None, "source": self.source, "roi": self.roi,
                    "classes": CLASSES}

    def image(self):
        with self.lock:
            if self.captured_at is None or time.monotonic() - self.captured_at > self.config["fresh_seconds"]:
                return None
            return self.jpeg

    def capture(self, label, split, session):
        if label not in CLASSES or split not in ("train", "val", "test"):
            raise ValueError("Selecciona una clase y un conjunto válidos.")
        if not isinstance(session, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", session):
            raise ValueError("La sesión debe tener de 1 a 40 letras, números, guiones o guiones bajos.")
        with self.lock:
            if self.crop is None or self.captured_at is None or time.monotonic() - self.captured_at > self.config["fresh_seconds"]:
                raise ValueError("No hay una imagen reciente para capturar. Inicia la cámara.")
            import cv2
            dataset = self.root / "dataset"
            dataset.mkdir(exist_ok=True)
            manifest_path = dataset / "sessions.json"
            sessions = json.loads(manifest_path.read_text("utf-8")) if manifest_path.exists() else {}
            if session in sessions and sessions[session] != split:
                raise ValueError("Esa sesión pertenece a otro conjunto. Usa sesiones distintas para evitar fuga de datos.")
            sessions[session] = split
            target = dataset / split / label
            target.mkdir(parents=True, exist_ok=True)
            name = session + "__" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f") + ".jpg"
            if not cv2.imwrite(str(target / name), self.crop):
                raise ValueError("No fue posible guardar la imagen.")
            temporary = manifest_path.with_suffix(".tmp")
            temporary.write_text(json.dumps(sessions, indent=2), "utf-8")
            temporary.replace(manifest_path)
            return f"Guardada: dataset/{split}/{label}/{name}"

    def _run(self, stop):
        capture = None
        try:
            try:
                import cv2
            except ImportError:
                raise RuntimeError("Falta OpenCV. Ejecuta instalar_vision.ps1 para habilitar la cámara.")
            model = None
            model_path = self.root / self.config["model_path"]
            model_error = "Modelo sin entrenar. Puedes capturar imágenes; los préstamos están bloqueados."
            if model_path.is_file():
                try:
                    os.environ.setdefault("YOLO_CONFIG_DIR", str(self.root / "data" / "ultralytics"))
                    from ultralytics import YOLO
                    model = YOLO(str(model_path), task="classify")
                    if set(model.names.values()) != set(CLASSES):
                        raise ValueError("El modelo debe contener exactamente martillo, destornillador, alicate, vacio y otros.")
                    self.model_ready = True
                    model_error = None
                except Exception as exc:
                    model = None
                    model_error = "No se pudo cargar el modelo: " + str(exc)[:250]
            if not model:
                self.engine.camera_unavailable(model_error)
            capture = cv2.VideoCapture(self.source, cv2.CAP_DSHOW if os.name == "nt" else cv2.CAP_ANY)
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            if not capture.isOpened():
                raise RuntimeError("No se pudo abrir la cámara. Inicia DroidCam y prueba otro índice.")
            self.status = "Cámara real · modelo activo" if model else model_error
            if model:
                self.inference_thread = threading.Thread(target=self._infer, args=(stop, model), daemon=True, name="inference")
                self.inference_thread.start()
            while not stop.is_set():
                ok, frame = capture.read()
                stamp = time.monotonic()
                if not ok or frame is None:
                    raise RuntimeError("Se perdió el video de la cámara. Reconecta DroidCam y vuelve a iniciar.")
                height, width = frame.shape[:2]
                x, y, w, h = self.roi
                left, top, right, bottom = int(x * width), int(y * height), int((x + w) * width), int((y + h) * height)
                crop = frame[top:bottom, left:right].copy()
                if crop.size == 0:
                    raise RuntimeError("La región de cámara está vacía.")
                # Letterbox cuadrado: conserva la herramienta completa con el CenterCrop del clasificador.
                size = max(crop.shape[:2])
                vertical, horizontal = size - crop.shape[0], size - crop.shape[1]
                square = cv2.copyMakeBorder(crop, vertical // 2, vertical - vertical // 2,
                                           horizontal // 2, horizontal - horizontal // 2,
                                           cv2.BORDER_CONSTANT, value=(30, 30, 30))
                preview = frame.copy()
                cv2.rectangle(preview, (left, top), (right - 1, bottom - 1), (80, 205, 155), 2)
                encoded_ok, encoded = cv2.imencode(".jpg", preview, [cv2.IMWRITE_JPEG_QUALITY, 78])
                with self.lock:
                    if stop.is_set():
                        break
                    self.frame_id += 1
                    if encoded_ok:
                        self.jpeg = encoded.tobytes()
                    self.crop, self.captured_at = square, stamp
                stop.wait(.015)
        except Exception as exc:
            with self.lock:
                if not stop.is_set():
                    self.status = str(exc)
                    self.engine.camera_unavailable(str(exc))
                self.jpeg = self.crop = self.captured_at = None
                self.model_ready = False
        finally:
            stop.set()
            if capture is not None:
                capture.release()

    def _infer(self, stop, model):
        """Consume siempre la captura más reciente; no acumula una cola de video."""
        last_id = -1
        try:
            while not stop.wait(.18):
                with self.lock:
                    if self.crop is None or self.frame_id == last_id:
                        continue
                    frame, stamp, frame_id = self.crop.copy(), self.captured_at, self.frame_id
                last_id = frame_id
                result = model.predict(frame, imgsz=224, device="cpu", verbose=False)[0]
                label = result.names[int(result.probs.top1)]
                confidence = float(result.probs.top1conf)
                with self.lock:
                    if not stop.is_set():
                        self.engine.observe(label, confidence, frame_id, stamp)
        except Exception as exc:
            with self.lock:
                self.model_ready = False
                self.status = "Inferencia detenida: " + str(exc)[:250]
                self.engine.camera_unavailable(self.status)

