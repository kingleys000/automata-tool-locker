#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -x .venv/bin/python ]]; then
  echo 'Ejecuta ./instalar.sh primero.' >&2
  exit 1
fi

.venv/bin/python -m pip install torch==2.14.1 torchvision==0.29.1 --index-url https://download.pytorch.org/whl/cpu
.venv/bin/python -m pip install -r requirements-vision.txt
echo 'Visión preparada. Captura imágenes desde el portal y consulta docs/RECONOCIMIENTO.md.'
