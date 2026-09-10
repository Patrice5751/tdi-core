param(
    [string]$DashboardDir = "C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files"
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

$StateFiles = @(
    (Join-Path $DashboardDir "XAUUSD.json"),
    (Join-Path $DashboardDir "ETHUSD.json"),
    (Join-Path $DashboardDir "intermarket_XAUUSD_XAGUSD.json")
)

$HealthCode = @'
from pathlib import Path
import sys

from tdi.services.live_health_checker import LiveHealthChecker

checker = LiveHealthChecker(stale_after_seconds=300)
files = [Path(value) for value in sys.argv[1:]]

sys.exit(1 if checker.requires_recovery(files) else 0)
'@

& $Python -c $HealthCode @StateFiles
$HealthResult = $LASTEXITCODE

if ($HealthResult -eq 0) {
    Write-Host "TDI Live HEALTHY"
    exit 0
}

if ($HealthResult -eq 1) {
    Write-Host "TDI Live STALE - recovery required"
    exit 1
}

Write-Host "TDI Live health check failed (exit code $HealthResult)"
exit 2
