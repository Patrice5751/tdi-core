Set-Location "C:\Projets\tdi-core"
$env:TDI_MT5_TERMINAL_PATH = "C:\Program Files\MetaTrader 5\terminal64.exe"

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$logDirectory = Join-Path $env:LOCALAPPDATA "TDI"
New-Item -ItemType Directory -Path $logDirectory -Force |
    Out-Null

$logFile = Join-Path $logDirectory "tdi_live.log"

$errorLogFile = Join-Path $logDirectory "tdi_live_error.log"

$existingTdi = Get-CimInstance Win32_Process |
    Where-Object {
        $_.Name -match '^python(\.exe)?$' -and
        $_.CommandLine -like '*scripts.run_tdi_mt5*' -and
        $_.CommandLine -like '*--monitor*'
    }

if ($existingTdi) {
    Write-Host "TDI Live est deja actif. Aucun second lancement."
    exit 0
}

$runnerArguments = @(
    "-u"
    "-m"
    "scripts.run_tdi_mt5"
    "XAUUSD"
    "XAGUSD"
    "NAS100"
    "EURUSD"
    "GBPUSD"
    "AUDUSD"
    "USDJPY"
    "USOUSD"
    "USDCAD"
    "BTCUSD"
    "ETHUSD"
    "SP500"
    "--monitor"
    "--interval"
    "60"
    "--dashboard-dir"
    "C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files"
)

Start-Process `
    -FilePath "C:\Projets\tdi-core\.venv\Scripts\python.exe" `
    -ArgumentList $runnerArguments `
    -WorkingDirectory "C:\Projets\tdi-core" `
    -WindowStyle Hidden `
    -RedirectStandardOutput $logFile `
    -RedirectStandardError $errorLogFile