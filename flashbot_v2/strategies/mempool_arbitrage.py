from .base_strategy import _SimpleStrategy
class MempoolArbitrage(_SimpleStrategy):
    def __init__(self): super().__init__("mempool_arbitrage", requires_flash=True, chains=["ethereum"])
