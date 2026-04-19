import argparse
import logging

from config import DEFAULT_URL, OUTPUT_DIR
from logging_config import setup_logging
from scraper import read_gadm_webpage
from downloader import download_zip_files
from geopackage_reader import read_geopackage
from unzipper import unzip_files
from utils import list_geopackage_files

def main():
    ## Application setup
    # Logging
    setup_logging()
    logger = logging.getLogger(__name__)

    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()

    ## Main logic
    # Download zip files from GADM website
    logger.info("Starting downloader")

    links = read_gadm_webpage(args.url)
    logger.info(f"Found {len(links)} links")

    download_zip_files(
        links,
        output_dir=OUTPUT_DIR,
        skip_existing=not args.overwrite
    )

    # Unzip downloaded files
    logger.info("Extracting downloaded zip files")

    unzip_files(
        input_dir=OUTPUT_DIR,
        output_dir=OUTPUT_DIR,
        overwrite=args.overwrite
    )

    # Get the newest GeoPackage file (assumes naming convention allows sorting by name)
    sorted_geopackage_files = list_geopackage_files(OUTPUT_DIR)
    first_geopackage_file = sorted_geopackage_files[0] if sorted_geopackage_files else None

    # Read the newest GeoPackage file
    gadm_global_sub_divisions = read_geopackage(first_geopackage_file) if first_geopackage_file else None
    if gadm_global_sub_divisions is not None:
        logger.info(f"First few rows of the GeoDataFrame:\n{gadm_global_sub_divisions.head()}")

    logger.info("Done")

if __name__ == "__main__":
    main()