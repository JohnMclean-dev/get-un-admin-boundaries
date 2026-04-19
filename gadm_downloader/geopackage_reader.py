import logging
from pathlib import Path
import geopandas as gpd

logger = logging.getLogger(__name__)

def read_geopackage(file_path: str | Path, layer: str | None = None) -> gpd.GeoDataFrame:
    """
    Read a GeoPackage file into a GeoDataFrame.

    Parameters
    ----------
    file_path : str | Path
        Path to the .gpkg file.
    layer : str | None
        Specific layer to read. If None, reads the first layer.

    Returns
    -------
    geopandas.GeoDataFrame
    """
    
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"GeoPackage not found: {file_path}")

    try:
        logger.info(f"Reading GeoPackage with pyogrio: {file_path}")

        gdf = gpd.read_file(
            file_path,
            layer=layer,
            engine="pyogrio"
        )

        logger.info(f"Loaded {len(gdf)} features")
        return gdf

    except Exception as e:
        logger.exception("Failed to read GeoPackage")
        raise RuntimeError(f"Error reading GeoPackage: {file_path}") from e