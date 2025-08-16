from __future__ import annotations
import logging
from typing import List, Optional
from core.types import Wallet

log = logging.getLogger("WalletManager")

class WalletManager:
    def __init__(self, wallets: List[Wallet]):
        self.wallets = wallets

    def add_wallet(self, wallet: Wallet):
        self.wallets.append(wallet)

    def get_best_wallet(self, chain: str) -> Wallet:
        for w in self.wallets:
            if w.chain == chain:
                return w
        raise ValueError(f"No wallet for chain {chain}")

    def label_wallet(self, wallet: Wallet, label: str):
        wallet.label = label

    def check_liquidity(self, wallet: Wallet) -> float:
        # TODO: interroger solde (Web3/Solana); stub:
        balance = 100.0
        log.info(f"{wallet.label}@{wallet.chain} liquidity≈{balance}")
        return balance
