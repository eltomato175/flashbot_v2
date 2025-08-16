from .base_strategy import _SimpleStrategy
class CrossChainArbitrage(_SimpleStrategy):
    def __init__(self): super().__init__("cross_chain_arbitrage", requires_flash=True, chains=["ethereum","polygon","bsc","solana"])
