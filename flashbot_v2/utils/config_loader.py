# utils/config_loader.py
from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

def load_config(path: str = "config/settings.json") -> Dict[str, Any]:
    """
    Charge la configuration JSON et injecte les secrets depuis .env si nécessaires.
    Retourne un dict de config.
    """
    load_dotenv()  # charge .env dans l'environnement si présent
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {p}")

    with p.open("r", encoding="utf-8") as f:
        cfg = json.load(f)

    # If wallet entries reference env vars for private keys, inject them:
    for w in cfg.get("WALLETS", []):
        env_key = w.get("private_key_env")
        if env_key:
            w["private_key"] = os.getenv(env_key, "")
    return cfg
