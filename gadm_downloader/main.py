import argparse
import logging
from pathlib import Path

from config import DEFAULT_URL, OUTPUT_DIR
from logging_config import setup_logging
from scraper import read_gadm_webpage
from downloader import download_zip_files
from geopackage_reader import read_geopackage
from unzipper import unzip_files

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

    # Read one of the downloaded GeoPackage files
    gdf = read_geopackage(Path(OUTPUT_DIR) / 'gadm_410-gpkg' / 'gadm_410.gpkg')
    logger.info(f"First few rows of the GeoDataFrame:\n{gdf.head()}")

    logger.info("Done")

if __name__ == "__main__":
    main()