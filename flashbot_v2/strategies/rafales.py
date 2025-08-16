from .base_strategy import _SimpleStrategy
class RafalesStrategy(_SimpleStrategy):
    def __init__(self): super().__init__("rafales", requires_flash=True, chains=["ethereum","polygon","bsc","solana"])
    def tune_for_cycle(self, cycle: int): pass