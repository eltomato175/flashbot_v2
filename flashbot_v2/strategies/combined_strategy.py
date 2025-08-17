from utils.failsafe import FailSafe

class CombinedStrategy:
    def __init__(self, strategies, min_profit=0.0):
        """
        strategies : liste de stratégies (instances héritant de BaseStrategy)
        min_profit : profit minimum requis pour exécuter le trade
        """
        self.strategies = strategies
        self.min_profit = min_profit
        self.failsafe = FailSafe()

    def execute(self, market_data: dict):
        """
        Exécute toutes les stratégies et enregistre leurs résultats.
        Retourne une liste des résultats acceptés.
        """
        results = []
        for strat in self.strategies:
            res = strat.execute(market_data)

            profit = res.get("profit", 0.0)
            self.failsafe.record_profit(profit)

            if profit >= self.min_profit:
                print(f"[OK] {strat.__class__.__name__} → {profit}")
                results.append(res)
            else:
                print(f"[Skip] {strat.__class__.__name__} pas assez rentable (profit {profit})")

        return results
