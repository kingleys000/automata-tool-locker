$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$projectPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $projectPython)) {
    Write-Host 'Primero ejecuta instalar.ps1 con Python 3.12 instalado.'
    exit 1
}
& $projectPython run.py
exit $LASTEXITCODE
