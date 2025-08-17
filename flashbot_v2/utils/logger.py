# utils/logger.py
from __future__ import annotations
import sys
import logging
from typing import Optional

# Force stdout to UTF-8 when possible (Windows)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

def setup_logger(name: str = "flashbot", level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    if not logger.handlers:
        fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(numeric_level)
        ch.setFormatter(logging.Formatter(fmt))
        logger.addHandler(ch)

        # optional file handler
        try:
            fh = logging.FileHandler("logs/flashbot.log", encoding="utf-8")
            fh.setLevel(numeric_level)
            fh.setFormatter(logging.Formatter(fmt))
            logger.addHandler(fh)
        except Exception:
            # continue if cannot create file (permissions)
            pass

    return logger
