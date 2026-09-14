param(
    [string]$DashboardDir = "C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files",
    [switch]$Recover
)

$ProductionDashboardDir = "C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files"

if ($Recover -and $DashboardDir -ne $ProductionDashboardDir) {
    Write-Host "Recovery aborted - non-production dashboard directory"
    exit 2
}

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

if ($HealthResult -eq 1 -and -not $Recover) {
    Write-Host "TDI Live STALE - recovery required"
    exit 1
}

if ($HealthResult -eq 1 -and $Recover) {
    Write-Host "TDI Live STALE - recovery requested"

    $TdiRoots = Get-CimInstance Win32_Process |
        Where-Object {
            $_.Name -eq "powershell.exe" -and
            $_.CommandLine -like '*-File "C:\Projets\tdi-core\start_tdi_live.ps1"*'
        }

    $RootCount = @($TdiRoots).Count

    if ($RootCount -gt 1) {
        Write-Host "Recovery aborted - expected at most 1 TDI root, found $RootCount"
        exit 2
    }

    if ($RootCount -eq 1) {
        $TdiRoot = @($TdiRoots)[0]

        Write-Host "Recovery authorized - TDI root PID $($TdiRoot.ProcessId)"

        Stop-ScheduledTask -TaskName "TDI Live"

        & taskkill.exe /PID $TdiRoot.ProcessId /T /F

        if ($LASTEXITCODE -ne 0) {
            Write-Host "Recovery failed - taskkill exit code $LASTEXITCODE"
            exit 2
        }

        Start-Sleep -Seconds 2
    }
    else {
        Write-Host "Recovery authorized - TDI Live is not running"
    }

    $RemainingTdi = Get-CimInstance Win32_Process |
        Where-Object {
            ($_.Name -match '^python(\.exe)?$' -and
             $_.CommandLine -like '*scripts.run_tdi_mt5*') -or
            ($_.Name -eq 'powershell.exe' -and
             $_.CommandLine -like '*start_tdi_live.ps1*')
        }

    if (@($RemainingTdi).Count -ne 0) {
        Write-Host "Recovery failed - TDI processes still running"
        exit 2
    }

    Write-Host "TDI Live stopped successfully"

    $SchedulerWaitSeconds = 15
    $SchedulerReady = $false

    for ($i = 0; $i -lt $SchedulerWaitSeconds; $i++) {
        $TaskState = (Get-ScheduledTask -TaskName "TDI Live").State

        if ($TaskState -ne "Running") {
            $SchedulerReady = $true
            break
        }

        Start-Sleep -Seconds 1
    }

    if (-not $SchedulerReady) {
        Write-Host "Recovery failed - scheduler still Running"
        exit 2
    }

    Start-ScheduledTask -TaskName "TDI Live"

    Write-Host "TDI Live restart requested"

    $RecoveryWaitSeconds = 120
    $Recovered = $false

    for ($i = 0; $i -lt $RecoveryWaitSeconds; $i += 5) {
        Start-Sleep -Seconds 5

        & $Python -c $HealthCode @StateFiles

        if ($LASTEXITCODE -eq 0) {
            $Recovered = $true
            break
        }
    }

    if (-not $Recovered) {
        Write-Host "Recovery failed - TDI Live did not become healthy"
        exit 2
    }

    Write-Host "TDI Live recovered successfully"
    exit 0
}

Write-Host "TDI Live health check failed (exit code $HealthResult)"
exit 2
