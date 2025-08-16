from .base_strategy import _SimpleStrategy
class PriceLeakageDetection(_SimpleStrategy):
    def __init__(self): super().__init__("price_leakage_detection", requires_flash=True, chains=["ethereum","solana"])
