import logging
import os
from datetime import datetime

def setup_logger():
    # Create logs directory if it doesn't exist
    log_dir = "data/logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"pacman_mas_{timestamp}.log")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    logger = logging.getLogger('PacManMAS')
    logger.info("=== Pac-Man Multi-Agent System Started ===")
    return logger
