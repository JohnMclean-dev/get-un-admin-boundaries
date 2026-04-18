#!/usr/bin/env python3
"""
GADM GeoJSON Downloader
"""

import argparse
import logging
import logging.handlers
import os
import sys
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

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

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(requests.RequestException),
    before_sleep=lambda retry_state: logger.warning(f"Retrying read_gadm_webpage (attempt {retry_state.attempt_number})...")
)
def read_gadm_webpage(url: str = "https://gadm.org/download_world.html") -> list(str):
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

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(requests.RequestException),
    before_sleep=lambda retry_state: logger.warning(
        f"Retrying download (attempt {retry_state.attempt_number})..."
    )
)
def download_zip_file(link: str, output_dir: str = "/app/output", skip_existing: bool = True) -> None:
    logger.info(f"Processing link: {link}")

    filename = get_filename_from_url(link)
    output_path = os.path.join(output_dir, filename)

    if should_skip_file(output_path, skip_existing):
        logger.warning(f"File already exists, skipping: {filename}")
        return None

    if os.path.exists(output_path):
        logger.info(f"File exists, overwriting: {filename}")

    try:
        response = fetch_stream(link)
        write_to_file(response, output_path)

        logger.info(f"Successfully downloaded: {filename}")
        return output_path

    except requests.RequestException as e:
        logger.error(f"Failed to download {link}: {e}")
        raise

    return None

def download_zip_files(links, skip_existing=True) -> None:
    """Download files from the provided links."""
    for link in links:
        download_zip_file(link, skip_existing=skip_existing)

    return None

def main() -> None:

    log_break=f"\n{'-'*50}"
    logger.info(f"{log_break}Starting GADM GeoJSON Downloader{log_break}")

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
    logger.info(f"Overwrite existing files: {args.overwrite}")

    download_links = read_gadm_webpage(args.url)
    logger.info(f"Total download links found: {len(download_links)}")

    download_zip_files(download_links, skip_existing=not args.overwrite)
    logger.info("All downloads completed.")

    logger.info(f"{log_break}Completed GADM GeoJSON Downloader{log_break}")

if __name__ == "__main__":
    main()