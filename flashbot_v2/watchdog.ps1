# watchdog.ps1
# Surveille FlashBot et le relance automatiquement en cas de crash

$BotPath = ".\.venv\Scripts\Activate.ps1"
$MainScript = "main.py"

while ($true) {
    try {
        Write-Host "$(Get-Date) - Lancement de FlashBot..."
        & $BotPath
        python $MainScript
    } catch {
        Write-Warning "$(Get-Date) - FlashBot a crashé, redémarrage dans 5s..."
        Start-Sleep -Seconds 5
    }
}
