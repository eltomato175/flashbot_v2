import logging


def setup_logger(name: str) -> logging.Logger:
    """
    Configure un logger global pour FlashBot
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
