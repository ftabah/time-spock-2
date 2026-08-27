$ErrorActionPreference = "Stop"

$python = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

$env:PYTHONPATH = Join-Path $PSScriptRoot "..\src"
& $python -m PyInstaller --noconfirm --clean --onefile --windowed --name TimeSpock src/time_spock/__main__.py

Write-Host "Executable created at dist\TimeSpock.exe"