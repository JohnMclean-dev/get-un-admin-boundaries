#!/usr/bin/env python3
"""
GADM GeoJSON Downloader
TODO: Implement application logic
"""

import argparse
import logging
import logging.handlers
import os
import sys
import requests
from bs4 import BeautifulSoup

# Configure logging
# Available levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
# Can be overridden via LOG_LEVEL environment variable
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

# Create rotating file handler (1MB max, keep 5 backup files)
file_handler = logging.handlers.RotatingFileHandler(
    "/app/logs/app.log",
    maxBytes=1_000_000,  # 1MB
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

logger = logging.getLogger(__name__)

def read_gadm_webpage(url = "https://gadm.org/download_world.html"):
    """Read the GADM webpage and extract download links."""
    logger.info(f"Reading {url}...")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        logger.info(f"Successfully fetched webpage (status: {response.status_code})")

        soup = BeautifulSoup(response.content, "html.parser")

        # Find all download links (zip files)
        links = soup.find_all("a", href=True)
        download_links = [link["href"] for link in links if link["href"].endswith(".zip")]

        logger.info(f"Found {len(download_links)} download links")
        for link in download_links:
            logger.debug(f"  - {link}")

        return download_links

    except requests.RequestException as e:
        logger.error(f"Failed to fetch webpage: {e}")
        return []

def get_download_links(links, skip_existing=True):
    """Download files from the provided links."""
    for link in links:
        logger.info(f"Processing link: {link}")
        try:
            response = requests.get(link, stream=True, timeout=60)
            response.raise_for_status()

            filename = os.path.basename(link)
            output_path = os.path.join("/app/output", filename)

            # Skip download if file already exists by default, unless skip_existing is False
            if os.path.exists(output_path):
                if skip_existing:
                    logger.warning(f"File already exists, skipping: {filename}")
                    continue
                else:
                    logger.info(f"File already exists, deleting (before re-writing): {filename}")
                    os.remove(output_path)

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"Successfully downloaded: {filename}")

        except requests.RequestException as e:
            logger.error(f"Failed to download {link}: {e}")

def main():

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="GADM GeoJSON Downloader")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrites existing files instead of skipping them (default: False)"
    )
    parser.add_argument(
        "--url",
        default="https://gadm.org/download_world.html",
        help="URL to fetch download links from (default: https://gadm.org/download_world.html)"
    )
    args = parser.parse_args()

    logger.info('Hello World! This is the GADM GeoJSON Downloader.')
    logger.info(f"Force download: {args.overwrite}")

    download_links = read_gadm_webpage(args.url)
    logger.info(f"Total download links found: {len(download_links)}")

    get_download_links(download_links, skip_existing=not args.overwrite)
    logger.info("All downloads completed.")

if __name__ == "__main__":
    main()