$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PidFile = Join-Path $ProjectRoot "runtime\tdi.pid"

if (-not (Test-Path $PidFile)) {
    Write-Host "TDI n'est pas actif."
    exit 0
}

$TdiPid = Get-Content $PidFile -ErrorAction SilentlyContinue

if (-not $TdiPid) {
    Remove-Item $PidFile -Force
    Write-Host "TDI n'est pas actif."
    exit 0
}

$Process = Get-Process -Id $TdiPid -ErrorAction SilentlyContinue

if (-not $Process) {
    Remove-Item $PidFile -Force
    Write-Host "TDI n'est pas actif (PID obsolete supprime)."
    exit 0
}

Stop-Process -Id $TdiPid

Remove-Item $PidFile -Force

Write-Host "TDI arrete (PID $TdiPid)."
