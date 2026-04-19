import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def get_filename_from_url(url: str) -> str:
    return os.path.basename(url)

def should_skip_file(path: str, skip_existing: bool) -> bool:
    return skip_existing and os.path.exists(path)

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