Set-Location "C:\Projets\tdi-core"

& ".\.venv\Scripts\Activate.ps1"

python -m scripts.run_tdi_mt5 `
    XAUUSD `
    XAGUSD `
    NAS100 `
    EURUSD `
    GBPUSD `
    --monitor `
    --interval 60 `
    --dashboard-dir "C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Files"