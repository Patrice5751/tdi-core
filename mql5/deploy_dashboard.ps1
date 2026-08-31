$source = Join-Path $PSScriptRoot "TDI_Dashboard.mq5"

$destination = "C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Indicators\TDI_Dashboard.mq5"

Write-Host "Source      : $source"
Write-Host "Destination : $destination"

if (-not (Test-Path $source)) {
    Write-Error "TDI_Dashboard.mq5 introuvable dans le projet."
    exit 1
}

if (-not (Test-Path (Split-Path $destination))) {
    Write-Error "Le dossier Indicators de MT5 est introuvable."
    exit 1
}

Write-Host "Verification OK."

$backup = "$destination.bak"

if (Test-Path $destination) {
    Copy-Item $destination $backup -Force
    Write-Host "Backup     : $backup"
}

Copy-Item $source $destination -Force

Write-Host "Deployment OK."