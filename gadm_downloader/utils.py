import os
import shutil
import logging
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)

def get_filename_from_url(url: str) -> str:
    return os.path.basename(url)

def should_skip_file(path: str, skip_existing: bool) -> bool:
    return skip_existing and os.path.exists(path)


def clear_directory(directory: str | Path):
    """
    Delete all contents of a directory (but keep the directory itself).
    """
    directory = Path(directory)

    if not directory.exists():
        logger.warning(f"Directory does not exist: {directory}")
        return

    logger.info(f"Clearing directory: {directory}")

    for item in directory.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception:
            logger.exception(f"Failed to delete {item}")
            raise


def unzip_files(input_dir: str | Path, output_dir: str | Path, skip_existing: bool = False) -> list[Path]:
    """
    Unzip all .zip files in input_dir into output_dir.

    Parameters
    ----------
    input_dir : str | Path
        Directory containing downloaded zip files.
    output_dir : str | Path
        Directory to extract files into.
    skip_existing : bool
        If True, leave existing archives.

    Returns
    -------
    list[Path]
        List of extracted file paths.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    zip_files = list(input_dir.glob("*.zip"))

    if not zip_files:
        logger.warning(f"No zip files found in {input_dir}")
        return []

    extracted_files = []

    for zip_path in zip_files:
        extract_path = output_dir / zip_path.stem

        if extract_path.exists() and skip_existing:
            logger.info(f"Skipping existing extraction: {extract_path}")
            continue

        logger.info(f"Extracting {zip_path.name} → {extract_path}")

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)

            extracted_files.extend(extract_path.rglob("*"))

        except zipfile.BadZipFile:
            logger.error(f"Corrupt zip file: {zip_path}")
        except Exception as e:
            logger.exception(f"Failed to extract {zip_path}")
            raise RuntimeError(f"Extraction failed: {zip_path}") from e

    logger.info(f"Extraction complete: {len(extracted_files)} files found")
    return extracted_files
    

def list_geopackage_files(directory: str | Path) -> list[Path]:
    """
    Recursively find all .gpkg files in a directory.

    Parameters
    ----------
    directory : str | Path
        Root directory to search

    Returns
    -------
    list[Path]
        List of GeoPackage file paths
    """
    directory = Path(directory)

    if not directory.exists():
        logger.warning(f"Directory does not exist: {directory}")
        return []

    gpkg_files = list(directory.rglob("*.gpkg"))
    gpkg_files = sorted(gpkg_files, key=lambda f: f.name, reverse=True)

    if not gpkg_files:
        logger.warning(f"No GeoPackage files found in {directory}")
    else:
        logger.info(f"Found {len(gpkg_files)} GeoPackage file(s)")

    return gpkg_files