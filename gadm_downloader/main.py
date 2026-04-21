import argparse
import logging

from config import DEFAULT_URL, OUTPUT_DIR
from logging_config import setup_logging
from scraper import read_gadm_webpage
from downloader import download_zip_files
from geopackage_reader import read_geopackage
from utils import clear_directory, unzip_files, list_geopackage_files

def main():
    ## Application setup
    # Logging
    setup_logging()
    logger = logging.getLogger(__name__)

    # Argument parsing
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--file-mode",
        choices=["skip", "overwrite", "refresh"],
        default="skip",
        help="How to handle existing files in the output directory"
    )

    parser.add_argument(
        "--db-mode",
        choices=["append", "truncate"],
        default="append",
        help="How to handle database writes"
    )

    parser.add_argument("--url", default=DEFAULT_URL)

    args = parser.parse_args()

    ## Main logic
    # Handle file mode
    if args.file_mode == "refresh":
        clear_directory(OUTPUT_DIR)
        skip_existing = False
    elif args.file_mode == "overwrite":
        skip_existing = False
    else:
        skip_existing = True

    # Download zip files from GADM website
    logging_bookmark = "-" * 90
    logging.info(logging_bookmark)
    logger.info("Starting downloader")

    links = read_gadm_webpage(args.url)
    logger.info(f"Found {len(links)} links")

    download_zip_files(
        links,
        output_dir=OUTPUT_DIR,
        skip_existing=skip_existing
    )

    # Unzip downloaded files
    logger.info("Extracting downloaded zip files")

    unzip_files(
        input_dir=OUTPUT_DIR,
        output_dir=OUTPUT_DIR,
        skip_existing=skip_existing
    )

    # Get the newest GeoPackage file (assumes naming convention allows sorting by name)
    sorted_geopackage_files = list_geopackage_files(OUTPUT_DIR)

    if not sorted_geopackage_files:
        logger.error("No GeoPackage files found after extraction")
        return

    first_geopackage_file = sorted_geopackage_files[0]
    logger.info(f"Using GeoPackage: {first_geopackage_file}")

    # Read the newest GeoPackage file
    gadm_global_sub_divisions = read_geopackage(first_geopackage_file)
    if gadm_global_sub_divisions is not None:
        logger.info(f"First few rows of the GeoDataFrame:\n{gadm_global_sub_divisions.head()}")

    # TODO: Set up database connection for next steps

    logger.info("Done")
    logging.info(logging_bookmark)

if __name__ == "__main__":
    main()