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
        choices=["create-if-new", "append", "truncate", "check-if-exists"],
        default="create-if-new",
        help=(
            "Database mode:\n"
            "create-if-new = create tables if missing, then insert\n"
            "append = insert into existing tables\n"
            "truncate = clear tables, then insert\n"
            "check-if-exists = verify tables exist, no writes"
        )
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

    # Get the newest GeoPackage file as defined by the GADM file naming convention
    sorted_geopackage_files = list_geopackage_files(OUTPUT_DIR)

    if not sorted_geopackage_files:
        logger.error("No GeoPackage files found after extraction")
        return

    first_geopackage_file = sorted_geopackage_files[0]
    logger.info(f"Using GeoPackage: {first_geopackage_file}")

    # Read GeoPackage
    gadm_global_sub_divisions = read_geopackage(first_geopackage_file)
    if gadm_global_sub_divisions is not None:
        logger.info(f"First few rows of discovered GeoPackage:\n{gadm_global_sub_divisions.head()}")

    # TODO: Implement actual database logic in the following blocks
    # DB handling
    logger.info(f"Database mode: {args.db_mode}")

    if args.db_mode == "create-if-new":
        logger.info("Ensuring tables exist (create if missing)")
        # create_tables_if_not_exist()

        if gadm_global_sub_divisions is not None:
            logger.info("Inserting data into database")
            # insert_data(gadm_global_sub_divisions)

    elif args.db_mode == "append":
        logger.info("Appending to existing tables")

        if gadm_global_sub_divisions is not None:
            logger.info("Inserting data into database")
            # insert_data(gadm_global_sub_divisions)

    elif args.db_mode == "truncate":
        logger.info("Truncating tables before insert")
        # truncate_tables()

        if gadm_global_sub_divisions is not None:
            logger.info("Inserting data into database")
            # insert_data(gadm_global_sub_divisions)

    elif args.db_mode == "check-if-exists":
        logger.info("Checking if required tables exist")
        # verify_tables_exist()

        logger.info("Check complete — no data written")

    logger.info("Done")
    logging.info(logging_bookmark)


if __name__ == "__main__":
    main()