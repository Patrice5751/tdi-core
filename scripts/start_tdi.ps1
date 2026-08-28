$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$Runner = Join-Path $ProjectRoot "scripts\run_tdi_mt5.py"
$RuntimeDir = Join-Path $ProjectRoot "runtime"
$PidFile = Join-Path $RuntimeDir "tdi.pid"
$LogFile = Join-Path $RuntimeDir "tdi.log"
$ErrorLogFile = Join-Path $RuntimeDir "tdi-error.log"

New-Item -ItemType Directory -Path $RuntimeDir -Force | Out-Null

if (Test-Path $PidFile) {
    $ExistingPid = Get-Content $PidFile -ErrorAction SilentlyContinue

    if ($ExistingPid -and (Get-Process -Id $ExistingPid -ErrorAction SilentlyContinue)) {
        Write-Host "TDI est deja actif (PID $ExistingPid)."
        exit 0
    }

    Remove-Item $PidFile -Force
}

$Process = Start-Process `
    -FilePath $Python `
    -ArgumentList @(
        "-u",
        $Runner,
        "XAUUSD",
        "--monitor",
        "--interval",
        "60"
    ) `
    -WorkingDirectory $ProjectRoot `
    -WindowStyle Hidden `
    -RedirectStandardOutput $LogFile `
    -RedirectStandardError $ErrorLogFile `
    -PassThru

$Process.Id | Set-Content $PidFile

Write-Host "TDI demarre (PID $($Process.Id))."
