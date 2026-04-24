import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"


def setup_logging():
    """
    Setup application-wide logging
    """

    # 🔒 Ensure logs directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    # 🔥 Unique log file per run
    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
    log_path = os.path.join(LOG_DIR, log_filename)

    # 🎯 Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # ❗ Prevent duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # 📁 File handler (with rotation)
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3
    )

    # 🖥️ Console handler
    console_handler = logging.StreamHandler()

    # 🎨 Formatter
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 🔗 Attach handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Logging system initialized")
    
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    return logger