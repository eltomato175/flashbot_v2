from __future__ import annotations
import logging, time
from typing import Optional
from core.types import Wallet
from strategies.base_strategy import BaseStrategy

log = logging.getLogger("FLFE")

class FlashLoanEngine:
    """
    FLFE – moteur Flash Loan modulaire
    - simulate_max_loan : calcule un montant max simulé (stub)
    - execute_flash_loan : orchestre le prêt flash + stratégie
    - hybrid_mode : combine fonds wallet + flash
    - run_rafale : exécutions en rafales (parallèles/séquentielles)
    """

    def __init__(self, rpc_map: dict):
        self.rpc = rpc_map

    def simulate_max_loan(self, token: str, chain: str) -> float:
        # TODO: brancher sources réelles (Aave, dYdX, Jupiter Flash, etc.)
        base = {"ethereum": 1000.0, "bsc": 800.0, "polygon": 600.0, "solana": 900.0}
        est = base.get(chain, 300.0)
        log.info(f"[Sim] max flash loan {token}@{chain} ≈ {est}")
        return est

    def execute_flash_loan(self, strategy: BaseStrategy, amount: float):
        # TODO: transaction bundle atomique + remboursement
        log.info(f"FLASH start {strategy.name} amount={amount}")
        time.sleep(0.1)
        res = strategy.execute(flash=True, amount=amount)
        log.info(f"FLASH end {strategy.name} -> {res}")
        return res

    def hybrid_mode(self, wallet: Wallet, strategy: BaseStrategy):
        # Combine solde wallet + flash (stub)
        flash_amt = self.simulate_max_loan("USDC", wallet.chain) * 0.5
        log.info(f"Hybrid using wallet={wallet.label} + flash={flash_amt}")
        return self.execute_flash_loan(strategy, flash_amt)

    def run_rafale(self, strategy: BaseStrategy, repeat: bool, modify_each: bool,
                   parallel: int = 1, max_cycles: int = 100):
        """
        Rafales: répéter exécutions tant que rentable (stub).
        parallel>1 : ici on les séquence (simple), à paralléliser plus tard.
        """
        cycle, last_profit = 0, 0.0
        while True:
            cycle += 1
            if modify_each:
                strategy.tune_for_cycle(cycle)  # hook modifiable par ChatGPT
            res = strategy.execute(flash=strategy.requires_flash, amount=strategy.suggest_amount())
            last_profit = res.get("profit", 0.0)
            log.info(f"Rafale {cycle}/{max_cycles} profit={last_profit}")
            if not repeat or cycle >= max_cycles or last_profit <= 0:
                break
        return {"cycles": cycle, "last_profit": last_profit}
