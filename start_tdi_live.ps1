Set-Location "C:\Projets\tdi-core"

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

& ".\.venv\Scripts\Activate.ps1"

python -m scripts.run_tdi_mt5 `
    XAUUSD `
    XAGUSD `
    NAS100 `
    EURUSD `
    GBPUSD `
    AUDUSD `
    USDJPY `
    USOUSD `
    USDCAD `
    BTCUSD `
    ETHUSD `
    --monitor `
    --interval 60 `
    --dashboard-dir "C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files"
