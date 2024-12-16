import logging

def setup_logger():
    logger = logging.getLogger("PHISHGUARD_Logger")
    logger.setLevel(logging.DEBUG)

    # Console handler for real-time logs
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # File handler for persistent logs
    file_handler = logging.FileHandler("email_processor.log")
    file_handler.setLevel(logging.DEBUG)

    # Log format
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()
