import json
import os


def load_config(path: str = "config/settings.json") -> dict:
    """
    Charge la configuration JSON (chemins, clés, tokens, RPC, etc.)
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)

    return config
