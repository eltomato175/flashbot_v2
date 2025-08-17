class TradeSimulator:
    def __init__(self, min_profit=0.0):
        """
        min_profit : profit minimum pour valider un trade (en unité du token ou %)
        """
        self.min_profit = min_profit

    def simulate_trade(self, strategy, wallet, market_data):
        """
        Simule le trade pour une stratégie sur un wallet
        Retourne profit simulé
        """
        # Ici tu peux mettre une logique simplifiée ou réelle selon DEX/API
        # Exemple factice : profit aléatoire
        import random
        simulated_profit = random.uniform(-1.0, 5.0)
        return simulated_profit

    def should_execute(self, profit):
        """
        Retourne True si le profit simulé dépasse le minimum configuré
        """
        return profit >= self.min_profit

