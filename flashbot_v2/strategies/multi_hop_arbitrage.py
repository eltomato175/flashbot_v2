from .base_strategy import _SimpleStrategy
class MultiHopArbitrage(_SimpleStrategy):
    def __init__(self): super().__init__("multi_hop_arbitrage", requires_flash=True, chains=["ethereum","polygon"])
