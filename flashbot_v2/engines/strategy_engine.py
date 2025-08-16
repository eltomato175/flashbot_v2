from __future__ import annotations
import logging
from typing import List, Dict, Type
from strategies.base_strategy import BaseStrategy

log = logging.getLogger("StrategyEngine")

class StrategyEngine:
    """
    IA Strategy Engine (simple heuristics now, pluggable with ML later)
    """

    def __init__(self, strategies: List[BaseStrategy]):
        self.strategies = strategies

    def evaluate_strategies(self, market_data: Dict) -> List[BaseStrategy]:
        # TODO: scorer via features; ici on vérifie is_active + health_check
        actives = [s for s in self.strategies if s.is_active and s.health_check()]
        log.info(f"Evaluate -> {len(actives)} active strategies")
        return actives

    def rank_strategies_by_profit(self, strategies: List[BaseStrategy]) -> List[BaseStrategy]:
        ranked = sorted(strategies, key=lambda s: s.estimate_profit(), reverse=True)
        log.info("Ranking: " + ", ".join(f"{s.name}:{s.estimate_profit():.4f}" for s in ranked))
        return ranked

    def disable_non_profitable(self, strategies: List[BaseStrategy]) -> List[BaseStrategy]:
        kept = [s for s in strategies if s.estimate_profit() > 0]
        log.info(f"Disable non-profitable -> kept {len(kept)}/{len(strategies)}")
        return kept

    def execute_strategy(self, strategy: BaseStrategy, auto: bool = True) -> dict:
        if auto:
            amt = strategy.suggest_amount()
            return strategy.execute(flash=strategy.requires_flash, amount=amt)
        return strategy.execute(flash=False, amount=0)
