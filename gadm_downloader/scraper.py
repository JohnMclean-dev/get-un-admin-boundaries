import requests
import logging
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(requests.RequestException),
)
def read_gadm_webpage(url: str) -> list[str]:
    logger.info(f"Reading {url}...")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a", href=True)

    download_links = [
        link["href"] for link in links
        if link["href"].endswith(".zip")
    ]

    logger.info(f"Found {len(download_links)} links")
    return download_links