import logging
from datetime import datetime

def setup_logging():
    """Configure application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('price_tracker.log'),
            logging.StreamHandler()
        ]
    )

def log_message(message, level='info'):
    """Log messages with timestamp"""
    logger = logging.getLogger(__name__)
    if level.lower() == 'error':
        logger.error(message)
    elif level.lower() == 'warning':
        logger.warning(message)
    else:
        logger.info(message)