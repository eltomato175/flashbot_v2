from .base_strategy import BaseStrategy

class MempoolStrategy(BaseStrategy):
    def __init__(self, name="MempoolStrategy", enabled=True):
        super().__init__(name, enabled)

    def evaluate(self, market_data):
        # Vérifie opportunités mempool
        return True

    def execute(self, wallet):
        print(f"Exécution Mempool Arbitrage sur {wallet}")
