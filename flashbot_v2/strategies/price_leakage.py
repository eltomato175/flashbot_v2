from .base_strategy import BaseStrategy

class PriceLeakageStrategy(BaseStrategy):
    def __init__(self, name="PriceLeakageStrategy", enabled=True):
        super().__init__(name, enabled)

    def evaluate(self, market_data):
        return True

    def execute(self, wallet):
        print(f"Exécution Price Leakage sur {wallet}")
