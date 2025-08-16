from __future__ import annotations
import logging
from typing import List
from strategies.base_strategy import BaseStrategy

log = logging.getLogger("MultiChain")

class MultiBlockchainEngine:
    def __init__(self, rpc_map: dict):
        self.rpc = rpc_map
        self.current = None

    def detect_supported_chains(self) -> List[str]:
        # TODO ping RPCs, jauger latence
        chains = [k for k, v in self.rpc.items() if v]
        log.info(f"Detected chains: {chains}")
        return chains

    def select_chain(self, chain_name: str):
        if chain_name not in self.rpc:
            raise ValueError(f"Unsupported chain {chain_name}")
        self.current = chain_name
        log.info(f"Selected chain -> {self.current}")

    def auto_select_chain(self, strategy: BaseStrategy):
        # TODO: sélectionner par latence/liquidité; stub -> première rentable
        preferred = strategy.preferred_chains() or self.detect_supported_chains()
        self.select_chain(preferred[0])
