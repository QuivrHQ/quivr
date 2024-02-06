import logging
from logging.handlers import RotatingFileHandler


def get_logger(logger_name, log_level=logging.INFO, log_file="application.log"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    logger.propagate = False  # Prevent log propagation to avoid double logging

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s [%(lineno)d]: %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=5000000, backupCount=5
    )  # 5MB file
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
