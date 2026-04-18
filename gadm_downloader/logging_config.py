import logging
import logging.handlers
import os
import sys
from config import LOG_FILE

def setup_logging():
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=1_000_000,
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            file_handler
        ]
    )