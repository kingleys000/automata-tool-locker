"""Ejecutar el módulo completamente simulado, independiente del portal de cámara."""
import argparse
from waitress import serve

from simulator.web import create_simulator


def main():
    parser = argparse.ArgumentParser(description="Simulador visual de autómatas")
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("El puerto debe estar entre 1 y 65535.")
    app = create_simulator(port=args.port, start_worker=True)
    print(f"Simulador: http://127.0.0.1:{args.port}/simulador", flush=True)
    print(f"Tablet: http://<IP-del-computador>:{args.port}/automatas", flush=True)
    print("Simulación completa. El estado de esta sesión se reinicia al cerrar el servidor.", flush=True)
    try:
        serve(app, host=args.host, port=args.port, threads=6)
    finally:
        app.extensions["worker_stop"].set()


if __name__ == "__main__":
    main()
