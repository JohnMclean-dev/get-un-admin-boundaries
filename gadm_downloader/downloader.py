import os
import logging
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config import CHUNK_SIZE
from utils import get_filename_from_url, should_skip_file

logger = logging.getLogger(__name__)

def fetch_stream(url: str):
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    return response

def write_to_file(response, output_path: str, chunk_size: int = CHUNK_SIZE):
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            f.write(chunk)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(requests.RequestException),
)
def download_zip_file(link: str, output_dir: str, skip_existing: bool = True):
    logger.info(f"Processing link: {link}")

    filename = get_filename_from_url(link)
    output_path = os.path.join(output_dir, filename)

    if should_skip_file(output_path, skip_existing):
        logger.warning(f"Skipping existing file: {filename}")
        return None

    if os.path.exists(output_path):
        logger.info(f"Overwriting file: {filename}")

    response = fetch_stream(link)
    write_to_file(response, output_path)

    logger.info(f"Downloaded: {filename}")
    return output_path


def download_zip_files(links: list[str], output_dir: str, skip_existing: bool):
    for link in links:
        download_zip_file(link, output_dir, skip_existing)