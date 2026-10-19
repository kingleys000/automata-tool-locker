$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$simulatorPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $simulatorPython)) {
    throw 'Primero ejecuta instalar.ps1 para preparar Python y el portal.'
}
& $simulatorPython run_simulador.py
exit $LASTEXITCODE
