from .base_strategy import _SimpleStrategy
class ArbitrageIntraDEX(_SimpleStrategy):
    def __init__(self): super().__init__("arbitrage_intra_dex", requires_flash=False, chains=["ethereum","polygon","bsc","solana"])