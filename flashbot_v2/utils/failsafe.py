import sys

class FailSafe:
    def __init__(self, loss_limit=-10.0, volatility_limit=0.15):
        """
        loss_limit : pertes max avant arrêt
        volatility_limit : indice de volatilité max autorisé
        """
        self.loss_limit = loss_limit
        self.volatility_limit = volatility_limit
        self.restart_requested = False

    def record_profit(self, profit: float):
        """Surveille les profits/pertes et déclenche un redémarrage si pertes trop élevées."""
        if profit < self.loss_limit:
            print(f"[FAILSAFE] Pertes trop élevées ({profit}), demande de redémarrage…")
            self.request_restart()

    def check_volatility(self, vol_idx: float):
        """Stoppe le bot si volatilité trop élevée."""
        if vol_idx > self.volatility_limit:
            print(f"[FAILSAFE] Volatilité trop élevée ({vol_idx}), stop trading.")
            self.request_restart()

    def request_restart(self):
        """Déclenche une sortie propre → superviseur redémarrera le bot."""
        self.restart_requested = True
        sys.exit(1)
