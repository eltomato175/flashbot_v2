from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    def __init__(self, use_flashloan=False, burst_mode=False):
        """
        use_flashloan : active l’utilisation de flashloan
        burst_mode : active la rafale (plusieurs trades groupés)
        """
        self.use_flashloan = use_flashloan
        self.burst_mode = burst_mode

    @abstractmethod
    def simulate(self, market_data: dict) -> dict:
        """
        Simule le trade.
        Retourne un dict { 'profit': float, 'details': str }
        """
        pass

    @abstractmethod
    def execute(self, market_data: dict) -> dict:
        """
        Exécute le trade réel.
        Retourne un dict { 'profit': float, 'tx': str }
        """
        pass
