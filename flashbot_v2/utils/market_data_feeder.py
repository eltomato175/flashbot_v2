from utils.failsafe import FailSafe

class MarketDataFeeder:
    def __init__(self):
        self.failsafe = FailSafe()

    def compute_volatility(self, prices: list[float]) -> float:
        """Calcule la volatilité et déclenche le FailSafe si besoin."""
        if not prices:
            return 0.0

        avg = sum(prices) / len(prices)
        variance = sum((p - avg) ** 2 for p in prices) / len(prices)
        vol_idx = (variance ** 0.5 / avg) if avg else 0.0

        # Hook FailSafe
        self.failsafe.check_volatility(vol_idx)

        return vol_idx
