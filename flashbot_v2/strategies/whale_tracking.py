from .base_strategy import _SimpleStrategy
class WhaleTracking(_SimpleStrategy):
    def __init__(self): super().__init__("whale_tracking", requires_flash=False, chains=["ethereum","solana","bsc"])
