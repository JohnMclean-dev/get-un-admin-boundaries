#!/usr/bin/env python3
"""
GADM GeoJSON Downloader

This script scrapes the GADM website (https://gadm.org/download_country.html)
and downloads all available GeoJSON files for each country.

Requirements:
- Selenium for browser automation
- Beautiful Soup for HTML parsing
- Chrome/Firefox webdriver
"""

import os
import time
import logging
from pathlib import Path
from typing import List, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)
from bs4 import BeautifulSoup
import requests


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GADMDownloader:
    """Scrapes GADM website and downloads GeoJSON files."""
    
    BASE_URL = "https://gadm.org/download_country.html"
    OUTPUT_DIR = Path("downloads")
    
    def __init__(self, browser: str = "chrome", headless: bool = True):
        """
        Initialize the downloader.
        
        Args:
            browser: Browser to use ('chrome' or 'firefox')
            headless: Run browser in headless mode
        """
        self.browser = browser
        self.headless = headless
        self.driver: Optional[webdriver.Remote] = None
        self.output_dir = self.OUTPUT_DIR
        self.output_dir.mkdir(exist_ok=True)
    
    def _get_driver(self) -> webdriver.Remote:
        """Create and configure the webdriver."""
        if self.browser.lower() == "chrome":
            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            driver = webdriver.Chrome(options=options)
        elif self.browser.lower() == "firefox":
            options = FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Unsupported browser: {self.browser}")
        
        driver.set_page_load_timeout(30)
        return driver
    
    def _wait_for_page_load(self, timeout: int = 10) -> bool:
        """Wait for the page to fully load."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            return True
        except TimeoutException:
            logger.warning("Page load timeout")
            return False
    
    def _get_page_soup(self) -> BeautifulSoup:
        """Get BeautifulSoup object from current page source."""
        return BeautifulSoup(self.driver.page_source, "html.parser")
    
    def _get_country_links(self) -> List[dict]:
        """Extract country names and their download links from the page."""
        countries = []
        soup = self._get_page_soup()
        
        # Look for download links - they typically contain "download" in href
        # and may be in tables or lists
        links = soup.find_all("a", href=True)
        
        for link in links:
            href = link.get("href", "")
            text = link.get_text(strip=True)
            
            # Check if this looks like a country download link
            # GADM links typically contain "download" or "gadm" in the URL
            if "download" in href.lower() or "gadm" in href.lower():
                # Try to extract country name from the link text or context
                country_name = text if text else self._extract_country_from_url(href)
                
                if country_name and href.startswith("http"):
                    countries.append({
                        "name": country_name,
                        "url": href
                    })
                elif href.startswith("http"):
                    # Try to get country name from parent elements
                    parent = link.find_parent(["tr", "li", "div"])
                    if parent:
                        # Look for country name in the row/cell
                        cell_text = parent.get_text(strip=True)
                        if cell_text:
                            countries.append({
                                "name": cell_text[:50],  # Limit length
                                "url": href
                            })
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_countries = []
        for country in countries:
            if country["url"] not in seen_urls:
                seen_urls.add(country["url"])
                unique_countries.append(country)
        
        logger.info(f"Found {len(unique_countries)} download links")
        return unique_countries
    
    def _extract_country_from_url(self, url: str) -> str:
        """Extract country name from URL."""
        # URL pattern: https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_XXX_geojson.zip
        parts = url.split("/")
        for part in parts:
            if "gadm" in part.lower() and "geojson" in part.lower():
                # Extract country code from gadm41_XXX
                try:
                    code = part.split("_")[1]
                    return code
                except IndexError:
                    pass
        return "unknown"
    
    def _find_download_buttons(self) -> List[dict]:
        """Find and click download buttons on the page."""
        downloads = []
        soup = self._get_page_soup()
        
        # Find all buttons/links that might be download buttons
        download_elements = soup.find_all("a", href=True)
        
        for elem in download_elements:
            href = elem.get("href", "")
            text = elem.get_text(strip=True)
            
            # Look for download-related links
            if any(keyword in href.lower() for keyword in ["download", "zip", "geojson"]):
                downloads.append({
                    "text": text,
                    "href": href
                })
        
        return downloads
    
    def _click_download_link(self, url: str) -> bool:
        """Click a download link and wait for download to complete."""
        try:
            # Navigate to the link
            self.driver.get(url)
            time.sleep(2)  # Wait for any redirect/download to start
            return True
        except WebDriverException as e:
            logger.error(f"Failed to click download link {url}: {e}")
            return False
    
    def _download_file(self, url: str, filename: str) -> bool:
        """Download a file directly via requests."""
        try:
            response = requests.get(url, timeout=60, stream=True)
            response.raise_for_status()
            
            filepath = self.output_dir / filename
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded: {filename}")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to download {url}: {e}")
            return False
    
    def _get_country_list_from_page(self) -> List[str]:
        """Get list of countries from the page."""
        countries = []
        soup = self._get_page_soup()
        
        # Look for country names in tables
        tables = soup.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                for cell in cells:
                    links = cell.find_all("a", href=True)
                    for link in links:
                        href = link.get("href", "")
                        text = link.get_text(strip=True)
                        if "download" in href.lower() and text:
                            countries.append(text)
        
        # Also check for select/option elements
        selects = soup.find_all("select")
        for select in selects:
            options = select.find_all("option")
            for option in options:
                text = option.get_text(strip=True)
                value = option.get("value", "")
                if value and text and value != text:
                    countries.append(text)
        
        return list(set(countries))
    
    def run(self) -> None:
        """Main method to run the scraper."""
        logger.info("Starting GADM GeoJSON downloader")
        
        try:
            # Initialize driver
            self.driver = self._get_driver()
            logger.info(f"Initialized {self.browser} driver")
            
            # Navigate to the main page
            logger.info(f"Loading {self.BASE_URL}")
            self.driver.get(self.BASE_URL)
            
            # Wait for page to load
            self._wait_for_page_load()
            time.sleep(3)  # Additional wait for dynamic content
            
            # Get country list
            countries = self._get_country_list_from_page()
            logger.info(f"Found {len(countries)} countries")
            
            # Get download links
            download_links = self._get_country_links()
            
            if not download_links:
                logger.warning("No download links found, trying alternative method")
                # Try clicking on the page to reveal download options
                self._try_alternative_scrape()
            
            # Download each file
            for link_info in download_links:
                url = link_info["url"]
                name = link_info["name"]
                
                # Generate filename from URL
                filename = url.split("/")[-1] or f"{name}.zip"
                
                logger.info(f"Downloading: {name}")
                success = self._download_file(url, filename)
                
                if success:
                    logger.info(f"Successfully downloaded: {name}")
                else:
                    logger.warning(f"Failed to download: {name}")
                
                time.sleep(1)  # Be polite to the server
            
            logger.info("Download complete!")
            
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            raise
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("Driver closed")
    
    def _try_alternative_scrape(self) -> List[dict]:
        """Try alternative methods to find download links."""
        logger.info("Trying alternative scraping method")
        
        # Get the page source and parse with BeautifulSoup
        soup = self._get_page_soup()
        
        # Look for any links that might be downloads
        all_links = soup.find_all("a", href=True)
        
        download_links = []
        for link in all_links:
            href = link.get("href", "")
            # Look for GeoJSON or download patterns
            if "geojson" in href.lower() or "zip" in href.lower():
                download_links.append({
                    "name": self._extract_country_from_url(href),
                    "url": href
                })
        
        if download_links:
            logger.info(f"Found {len(download_links)} links via alternative method")
        
        return download_links


def main():
    """Entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Download GeoJSON files from GADM"
    )
    parser.add_argument(
        "--browser",
        choices=["chrome", "firefox"],
        default="chrome",
        help="Browser to use for scraping"
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Run browser in visible mode (not headless)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="downloads",
        help="Output directory for downloads"
    )
    
    args = parser.parse_args()
    
    # Create downloader instance
    downloader = GADMDownloader(
        browser=args.browser,
        headless=not args.no_headless
    )
    
    # Update output directory if specified
    if args.output:
        downloader.output_dir = Path(args.output)
        downloader.output_dir.mkdir(exist_ok=True)
    
    # Run the downloader
    downloader.run()


if __name__ == "__main__":
    main()