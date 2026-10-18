$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$projectPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $projectPython)) { throw 'Ejecuta instalar.ps1 primero.' }
& $projectPython -m pip install -r requirements-vision.txt
if ($LASTEXITCODE -ne 0) { throw 'No se completó la instalación de visión artificial.' }
Write-Host 'Visión preparada. Captura imágenes desde el portal y consulta docs/RECONOCIMIENTO.md.'
