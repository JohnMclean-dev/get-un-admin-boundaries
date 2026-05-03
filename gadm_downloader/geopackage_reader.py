import logging
from pathlib import Path
import duckdb

logger = logging.getLogger(__name__)

def read_geopackage(file_path: str | Path, layer: str | None = None) -> duckdb.DuckDBPyRelation:
    """
    Read a GeoPackage file into a DuckDB relation.

    Uses DuckDB spatial extension for efficient reading without loading into memory.

    Parameters
    ----------
    file_path : str | Path
        Path to the .gpkg file.
    layer : str | None
        Specific layer to read. If None, reads the first layer.

    Returns
    -------
    duckdb.DuckDBPyRelation
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"GeoPackage not found: {file_path}")

    logger.info(f"Reading GeoPackage: {file_path}")

    # Create DuckDB connection
    con = duckdb.connect()

    # Install and load spatial extension
    con.install_extension("spatial")
    con.load_extension("spatial")

    try:
        # Read GeoPackage
        if layer:
            query = f"SELECT * FROM st_read('{file_path}', layer='{layer}')"
        else:
            query = f"SELECT * FROM st_read('{file_path}')"

        rel = con.sql(query)

        # Get count without materializing
        count = rel.count("*").fetchone()[0]
        logger.info(f"Loaded {count} features using DuckDB spatial extension")

        return rel
    except Exception as e:
        logger.exception("DuckDB spatial read failed")
        raise RuntimeError(
            f"Error reading GeoPackage with DuckDB spatial extension: {file_path}"
        ) from e