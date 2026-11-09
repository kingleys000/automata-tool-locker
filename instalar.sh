#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ -n "${PYTHON:-}" ]]; then
  base_python="$PYTHON"
elif [[ -x .tools/python312/bin/python3 ]]; then
  base_python=.tools/python312/bin/python3
elif command -v python3.12 >/dev/null 2>&1; then
  base_python=python3.12
else
  echo 'No se encontró un intérprete base. Define PYTHON o instala Python 3.12.' >&2
  exit 1
fi

"$base_python" -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
echo 'Portal preparado. Ejecuta ./iniciar.sh. Para cámara y modelo, ejecuta ./instalar_vision.sh.'
