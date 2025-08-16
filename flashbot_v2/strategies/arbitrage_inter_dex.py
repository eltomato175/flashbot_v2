from .base_strategy import _SimpleStrategy
class ArbitrageInterDEX(_SimpleStrategy):
    def __init__(self): super().__init__("arbitrage_inter_dex", requires_flash=True, chains=["ethereum","polygon","bsc"])
