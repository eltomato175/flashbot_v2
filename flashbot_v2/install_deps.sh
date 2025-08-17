#!/bin/bash
echo "=== Installation des dépendances FlashBot (Linux/Ubuntu) ==="

# Vérifie Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 n'est pas installé."
    exit 1
fi

# Crée venv si inexistant
if [ ! -d ".venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv .venv
fi

# Active venv
source .venv/bin/activate

# Upgrade pip
echo "Mise à jour de pip..."
pip install --upgrade pip setuptools wheel

# Installe requirements Linux
echo "Installation des dépendances Linux..."
pip install -r requirements_linux.txt

echo "✅ Installation terminée. Pour lancer le bot :"
echo "source .venv/bin/activate"
echo "python main.py"
