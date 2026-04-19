import logging
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)


def unzip_files(input_dir: str | Path, output_dir: str | Path, overwrite: bool = False) -> list[Path]:
    """
    Unzip all .zip files in input_dir into output_dir.

    Parameters
    ----------
    input_dir : str | Path
        Directory containing downloaded zip files.
    output_dir : str | Path
        Directory to extract files into.
    overwrite : bool
        If True, re-extracts existing archives.

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

        if extract_path.exists() and not overwrite:
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