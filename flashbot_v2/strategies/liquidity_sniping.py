from .base_strategy import _SimpleStrategy
class LiquiditySniping(_SimpleStrategy):
    def __init__(self): super().__init__("liquidity_sniping", requires_flash=True, chains=["ethereum","bsc"])
