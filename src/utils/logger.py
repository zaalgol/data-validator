import logging
from config.config_loader import config

def get_logger(name):
    """
    Configure and return a logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Set the logging level based on configuration
        logger.setLevel(getattr(logging, config.log_level.upper(), logging.INFO))

        # Define formatter for log messages
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # File handler to write logs to a file
        file_handler = logging.FileHandler(config.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler to output logs to the console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
