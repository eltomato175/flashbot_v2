#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "$0")"
if [ ! -d ".venv" ]; then
  python -m venv .venv
  . .venv/bin/activate
  python -m pip install --upgrade pip
  pip install -r requirements.txt
else
  . .venv/bin/activate
fi
python main.py
