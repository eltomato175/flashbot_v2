from utils.config_loader import load_config
from utils.logger import setup_logger
from strategies import FlashLoanStrategy, ArbitrageStrategy, MultiHopStrategy


def main():
    logger = setup_logger("FlashBot")
    config = load_config()

    logger.info("🚀 FlashBot v2 starting with config loaded")

    # Initialisation des stratégies
    strategies = [
        FlashLoanStrategy(),
        ArbitrageStrategy(),
        MultiHopStrategy()
    ]

    # Simulation de données marché (placeholder)
    market_data = {
        "eth_price": 1800,
        "sol_price": 24,
        "bnb_price": 240
    }

    # Exécution séquentielle des stratégies
    for strat in strategies:
        strat.run(market_data)


if __name__ == "__main__":
    main()
