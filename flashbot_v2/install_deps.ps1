# install_deps.ps1
Write-Host "=== Installation des dépendances FlashBot (Windows) ==="

# Vérifie Python
if (-Not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python n'est pas installé ou pas dans le PATH."
    exit 1
}

# Crée venv s'il n'existe pas
if (-Not (Test-Path ".venv")) {
    Write-Host "Création de l'environnement virtuel..."
    python -m venv .venv
}

# Active venv
Write-Host "Activation de l'environnement virtuel..."
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Mise à jour de pip..."
pip install --upgrade pip setuptools wheel

# Installe requirements Windows
Write-Host "Installation des dépendances Windows..."
pip install -r requirements_windows.txt

Write-Host "✅ Installation terminée. Pour lancer le bot :"
Write-Host ".\.venv\Scripts\Activate.ps1"
Write-Host "python main.py"
