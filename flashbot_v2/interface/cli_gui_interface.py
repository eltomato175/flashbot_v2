from __future__ import annotations
import argparse, json, logging
from pathlib import Path

def make_cli():
    p = argparse.ArgumentParser("FlashBot CLI")
    p.add_argument("--settings", default="config/settings.json")
    p.add_argument("--list-strategies", action="store_true")
    p.add_argument("--run-once", action="store_true", help="execute best strategy once")
    return p

def run_cli(args, strategies):
    if args.list_strategies:
        print("Strategies:", ", ".join(s.name for s in strategies))
    if args.run_once and strategies:
        s0 = sorted(strategies, key=lambda s: s.estimate_profit(), reverse=True)[0]
        print(f"Executing {s0.name}…", s0.execute(flash=s0.requires_flash, amount=s0.suggest_amount()))

# --- Simple GUI (run separately): streamlit run interface/cli_gui_interface.py
if __name__ == "__main__":
    import streamlit as st
    st.set_page_config(page_title="FlashBot v1", layout="wide")
    st.title("FlashBot v1 – Dashboard")
    st.write("Remplis config/settings.json, démarre main.py pour le backend/Telegram.")
    cfgp = Path("../config/settings.json")
    if cfgp.exists():
        st.json(json.loads(cfgp.read_text()))
    else:
        st.warning("config/settings.json manquant")
