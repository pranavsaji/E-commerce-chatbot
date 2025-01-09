import logging

def setup_logger():
    """Setup logging configuration."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    return logger
