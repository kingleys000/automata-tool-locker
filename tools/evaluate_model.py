"""Métricas reproducibles sobre test; no ajusta el modelo ni el umbral."""
import argparse
import csv
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.automata import CLASSES


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=ROOT / "dataset" / "test")
    parser.add_argument("--model", type=Path, default=ROOT / "models" / "herramientas.pt")
    args = parser.parse_args()
    if not args.model.is_file():
        print("Falta models/herramientas.pt. Captura imágenes y entrena primero.")
        return 2
    paths = [(label, p) for label in CLASSES for p in (args.data / label).glob("*") if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
    if not paths or any(not any(truth == label for truth, _ in paths) for label in CLASSES):
        print("El conjunto test debe incluir imágenes nuevas de las cinco clases.")
        return 2
    os.environ.setdefault("YOLO_CONFIG_DIR", str(ROOT / "data" / "ultralytics"))
    from ultralytics import YOLO
    model = YOLO(str(args.model), task="classify")
    if set(model.names.values()) != set(CLASSES):
        raise ValueError("Modelo con clases incompatibles.")
    threshold = json.loads((ROOT / "config.json").read_text("utf-8"))["confidence"]
    confusion = {truth: {pred: 0 for pred in CLASSES} for truth in CLASSES}
    results = []
    for truth, path in paths:
        result = model.predict(str(path), imgsz=224, device="cpu", verbose=False)[0]
        predicted, confidence = result.names[int(result.probs.top1)], float(result.probs.top1conf)
        confusion[truth][predicted] += 1
        results.append({"file":str(path), "truth":truth, "predicted":predicted, "confidence":confidence,
                        "would_accept_hammer_frame":predicted == "martillo" and confidence >= threshold})
    report = {"images":len(results), "accuracy":sum(r["truth"] == r["predicted"] for r in results) / len(results),
              "false_hammer_frames":sum(r["would_accept_hammer_frame"] and r["truth"] != "martillo" for r in results),
              "threshold":threshold, "confusion":confusion,
              "note":"Métricas de imágenes individuales. No sustituyen las pruebas temporales ni diez ciclos con cámara real."}
    output = ROOT / "artifacts"
    output.mkdir(exist_ok=True)
    (output / "evaluacion_modelo.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), "utf-8")
    with (output / "predicciones.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
