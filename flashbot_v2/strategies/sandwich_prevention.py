from .base_strategy import _SimpleStrategy
class SandwichPrevention(_SimpleStrategy):
    def __init__(self): super().__init__("sandwich_prevention", requires_flash=False, chains=["ethereum","polygon"])
