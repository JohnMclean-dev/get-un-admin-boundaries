#!/usr/bin/env python3
"""
GADM GeoJSON Downloader
TODO: Implement application logic
"""

import logging
import sys

# Configure logging
# Available levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("/app/logs/app.log")
    ]
)

logger = logging.getLogger(__name__)


def main():

    logger.info('Hello World! This is the GADM GeoJSON Downloader.')


if __name__ == "__main__":
    main()