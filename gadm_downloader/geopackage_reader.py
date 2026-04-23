import logging
from pathlib import Path
import geopandas as gpd

logger = logging.getLogger(__name__)

def read_geopackage(file_path: str | Path, layer: str | None = None) -> gpd.GeoDataFrame:
    """
    Read a GeoPackage file into a GeoDataFrame.

    Tries the default GeoPandas engine first (usually pyogrio if available),
    and falls back to Fiona if the first attempt fails.

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

    logger.info(f"Reading GeoPackage: {file_path}")

    # 1st attempt: default engine (usually pyogrio if installed)
    try:
        gdf = gpd.read_file(file_path, layer=layer)
        logger.info(f"Loaded {len(gdf)} features using default engine")
        return gdf

    except Exception as e:
        logger.warning(
            f"Default GeoPandas engine failed for {file_path}. "
            f"Retrying with Fiona. Error: {e}"
        )

    # 2nd attempt: explicit Fiona fallback
    try:
        gdf = gpd.read_file(file_path, layer=layer, engine="fiona")
        logger.info(f"Loaded {len(gdf)} features using Fiona engine")
        return gdf

    except Exception as e:
        logger.exception("Both GeoPandas engines failed")
        raise RuntimeError(
            f"Error reading GeoPackage (both engines failed): {file_path}"
        ) from e