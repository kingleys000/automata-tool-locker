$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$projectPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $projectPython)) {
    & py -3.12 -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Instala Python 3.12 de python.org y vuelve a ejecutar este archivo.' }
}
& $projectPython -m pip install -r requirements-dev.txt
if ($LASTEXITCODE -ne 0) { throw 'No se completó la instalación. Revisa la conexión a internet.' }
Write-Host 'Portal preparado. Ejecuta iniciar.ps1. Para cámara y modelo, ejecuta instalar_vision.ps1.'
