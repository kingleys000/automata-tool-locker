"""Ejecutar: python run.py. El control solo admite conexiones de loopback."""
import argparse
import json
from pathlib import Path

from app.web import create_app


def main():
    parser = argparse.ArgumentParser(description="Portal local de autómatas y herramientas")
    parser.add_argument("--port", type=int)
    parser.add_argument("--host", help="Usa 127.0.0.1 para limitar las pruebas al computador")
    args = parser.parse_args()
    config = json.loads(Path(__file__).with_name("config.json").read_text("utf-8"))
    if args.port:
        config["port"] = args.port
    if args.host:
        config["host"] = args.host
    app = create_app(config, start_worker=True)
    print(f"Control: http://127.0.0.1:{config['port']}/control", flush=True)
    print(f"Tablet: http://<IP-del-computador>:{config['port']}/monitor", flush=True)
    print("Puerta y sensores simulados. La cámara solo se inicia desde el control.", flush=True)
    from waitress import serve
    serve(app, host=config["host"], port=config["port"], threads=6)


if __name__ == "__main__":
    main()
