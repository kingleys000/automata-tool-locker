#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -x .venv/bin/python ]]; then
  echo 'Primero ejecuta ./instalar.sh con Python 3.12 disponible.' >&2
  exit 1
fi
exec .venv/bin/python run.py
