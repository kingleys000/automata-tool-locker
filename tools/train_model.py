"""Entrena exclusivamente con imágenes propias; no instala ni inventa un dataset."""
import argparse
import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.automata import CLASSES


def inspect_dataset(dataset):
    counts = {}
    sessions = {}
    errors = []
    for split in ("train", "val", "test"):
        counts[split] = {}
        for label in CLASSES:
            files = sorted(path for path in (dataset / split / label).glob("*") if path.suffix.lower() in (".jpg", ".jpeg", ".png"))
            counts[split][label] = len(files)
            minimum = 10 if split == "train" else 5
            if len(files) < minimum:
                errors.append(f"{split}/{label}: {len(files)} imágenes; mínimo inicial {minimum}.")
            for path in files:
                if "__" not in path.name:
                    errors.append(f"{path.name}: usa nombres sesion__imagen.jpg para comprobar separación de sesiones.")
                    continue
                session = path.name.split("__", 1)[0]
                if session in sessions and sessions[session] != split:
                    errors.append(f"Sesión {session} mezclada entre {sessions[session]} y {split}.")
                sessions[session] = split
        if (dataset / split).exists():
            unexpected = [p.name for p in (dataset / split).iterdir() if p.is_dir() and p.name not in CLASSES]
            if unexpected:
                errors.append(f"Clases inesperadas en {split}: {', '.join(unexpected)}")
    return counts, sorted(set(errors))


def main():
    parser = argparse.ArgumentParser(description="Entrenar YOLO11n-cls con herramientas propias")
    parser.add_argument("--data", type=Path, default=ROOT / "dataset")
    parser.add_argument("--epochs", type=int, default=40)
    parser.add_argument("--device", default="cpu", help="cpu, o 0 si dispones de GPU compatible")
    parser.add_argument("--check", action="store_true", help="Solo validar estructura, sin descargar modelo ni entrenar")
    args = parser.parse_args()
    data = args.data.resolve()
    counts, errors = inspect_dataset(data)
    print(json.dumps(counts, ensure_ascii=False, indent=2))
    if errors:
        print("\nDataset todavía incompleto:\n- " + "\n- ".join(errors))
        return 2
    if args.check:
        print("Estructura y separación de sesiones correctas. Revisa visualmente las etiquetas.")
        return 0
    if args.epochs < 1:
        parser.error("epochs debe ser positivo")
    os.environ.setdefault("YOLO_CONFIG_DIR", str(ROOT / "data" / "ultralytics"))
    try:
        import cv2
        from ultralytics import YOLO
    except ImportError:
        print("Instala primero requirements-vision.txt.")
        return 2
    for path in data.rglob("*"):
        if path.suffix.lower() in (".jpg", ".jpeg", ".png") and cv2.imread(str(path)) is None:
            print(f"Imagen no legible: {path}")
            return 2
    # Puede descargar el peso base la primera vez. Los cinco tipos se aprenden
    # con el dataset del proyecto, no con etiquetas genéricas de ImageNet.
    model = YOLO("yolo11n-cls.pt")
    model.train(data=str(data), epochs=args.epochs, imgsz=224, batch=16,
                device=args.device, workers=0, seed=42, patience=10,
                project=str(ROOT / "runs"), name="herramientas", exist_ok=True,
                scale=0.0, fliplr=.5, auto_augment=None, erasing=0.0)
    destination = ROOT / "models"
    destination.mkdir(exist_ok=True)
    best = Path(model.trainer.best)
    if not best.is_file():
        print("El entrenamiento no produjo un modelo best.pt.")
        return 1
    trained = YOLO(str(best), task="classify")
    if set(trained.names.values()) != set(CLASSES):
        raise RuntimeError("El modelo resultante no contiene las cinco clases previstas.")
    shutil.copy2(best, destination / "herramientas.pt")
    metadata = {"base": "yolo11n-cls.pt", "classes": trained.names, "counts": counts,
                "epochs_requested": args.epochs, "input_size": 224, "seed": 42,
                "evaluation": "Pendiente: ejecutar tools/evaluate_model.py; no usar test para ajustar umbral."}
    (destination / "entrenamiento.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), "utf-8")
    print("Modelo guardado en models/herramientas.pt. Reinicia la cámara para cargarlo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
