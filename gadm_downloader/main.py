import argparse
import logging
from db import create_db_engine, test_connection
from pathlib import Path

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

    # TODO: rethink file mode options
    parser.add_argument(
        "--file-mode",
        choices=["skip", "overwrite", "refresh", "read"],
        default="skip",
        help=(
            "How to handle existing files in the output directory:\n"
            "skip = use existing files if present\n"
            "overwrite = re-download without clearing\n"
            "refresh = clear directory and re-download\n"
            "read = skip scraping/downloading and only read existing files"
        )
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

    logging_bookmark = "-" * 90
    logger.info(logging_bookmark)

    ## READ MODE (skip web scraping entirely)
    if args.file_mode == "read":
        logger.info("File mode: READ (skipping scrape, download, and unzip)")

        sorted_geopackage_files = list_geopackage_files(OUTPUT_DIR)

        if not sorted_geopackage_files:
            logger.error("No GeoPackage files found in output directory")
            return

        first_geopackage_file = sorted_geopackage_files[0]
        logger.info(f"Using existing GeoPackage: {first_geopackage_file}")

        gadm_global_sub_divisions = read_geopackage(first_geopackage_file)
        if gadm_global_sub_divisions is not None:
            logger.info(
                f"First few rows of discovered GeoPackage:\n"
                f"{gadm_global_sub_divisions.head()}"
            )

    ## NORMAL MODES (scrape + download + unzip)
    else:
        # Handle file mode
        if args.file_mode == "refresh":
            clear_directory(OUTPUT_DIR)
            skip_existing = False
        elif args.file_mode == "overwrite":
            skip_existing = False
        else:
            skip_existing = True

        logger.info("Starting downloader")

        links = read_gadm_webpage(args.url)
        logger.info(f"Found {len(links)} links")

        download_zip_files(
            links,
            output_dir=OUTPUT_DIR,
            skip_existing=skip_existing
        )

        logger.info("Extracting downloaded zip files")

        unzip_files(
            input_dir=OUTPUT_DIR,
            output_dir=OUTPUT_DIR,
            skip_existing=skip_existing
        )

        sorted_geopackage_files = list_geopackage_files(OUTPUT_DIR)

        if not sorted_geopackage_files:
            logger.error("No GeoPackage files found after extraction")
            return

        first_geopackage_file = sorted_geopackage_files[0]
        logger.info(f"Using GeoPackage: {first_geopackage_file}")

        gadm_global_sub_divisions = read_geopackage(first_geopackage_file)
        if gadm_global_sub_divisions is not None:
            logger.info(
                f"First few rows of discovered GeoPackage:\n"
                f"{gadm_global_sub_divisions.head()}"
            )

    logger.info(f"Database mode: {args.db_mode}")

    # Establish database connection
    engine = create_db_engine()

    if not test_connection(engine):
        logger.error("Exiting due to database connection failure")
        return

    # TODO: 0 - Create tables if needed
    if args.db_mode == "create-if-new":
        logger.info("Ensuring tables exist (create if missing)")

        if gadm_global_sub_divisions is not None:
            try:
                table_name = Path(first_geopackage_file).stem

                logger.info(f"Writing to table: {table_name}")

                gadm_global_sub_divisions.to_postgis(
                    name=table_name,
                    con=engine,
                    if_exists="append",   # creates table if it doesn't exist
                    index=False
                )

                logger.info("Insert successful")

            except Exception as e:
                logger.exception(f"Failed to insert data: {e}")
                return

    # TODO: 1 - Append data to existing tables
    elif args.db_mode == "append":
        logger.info("Appending to existing tables")

        if gadm_global_sub_divisions is not None:
            logger.info("Inserting data into database")

    # TODO: 2 - Truncate tables before insert
    elif args.db_mode == "truncate":
        logger.info("Truncating tables before insert")

        if gadm_global_sub_divisions is not None:
            logger.info("Inserting data into database")

    logger.info("Done")
    logger.info(logging_bookmark)


if __name__ == "__main__":
    main()