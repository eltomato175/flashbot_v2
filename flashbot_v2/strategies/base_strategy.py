from __future__ import annotations
import logging, random
from abc import ABC, abstractmethod
from typing import List

log = logging.getLogger("Strategy")

class BaseStrategy(ABC):
    name: str = "base_strategy"
    requires_flash: bool = False
    is_active: bool = True

    def __init__(self, chain: str | None = None):
        self.chain = chain

    @abstractmethod
    def preferred_chains(self) -> List[str]:
        return []

    @abstractmethod
    def estimate_profit(self) -> float:
        """Renvoie profit attendu (stub en %)"""
        return 0.0

    @abstractmethod
    def execute(self, flash: bool, amount: float) -> dict:
        """Exécute la stratégie (stub)"""
        return {"ok": True, "profit": 0.0}

    def health_check(self) -> bool:
        return True

    def suggest_amount(self) -> float:
        return 10.0

    def tune_for_cycle(self, cycle: int):
        # Hook pour Rafales (modifiable via ChatGPT)
        pass

# Helper pour fabriquer des stubs rapidement
class _SimpleStrategy(BaseStrategy):
    def __init__(self, name, requires_flash=False, chains=None):
        super().__init__()
        self.name = name
        self.requires_flash = requires_flash
        self._chains = chains or []

    def preferred_chains(self): return self._chains
    def estimate_profit(self): return round(random.uniform(-0.002, 0.01), 6)
    def execute(self, flash, amount):
        p = self.estimate_profit() * amount
        log.info(f"{self.name}: flash={flash} amount={amount} profit≈{p:.4f}")
        return {"ok": True, "profit": p}
