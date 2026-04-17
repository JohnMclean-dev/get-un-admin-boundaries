# GADM GeoJSON Downloader

A Python web scraping application wrapped in a Podman container that downloads GeoJSON administrative boundary files from [GADM](https://gadm.org).

## Overview

This application uses Selenium and Beautiful Soup to:
1. Navigate to https://gadm.org/download_country.html
2. Extract the list of available countries
3. Find and click download links
4. Download all available GeoJSON files (levels 0-4 depending on country)

## Requirements

- Python 3.11+
- Podman (for containerized execution)
- Chrome or Firefox browser

## Local Development

### 1. Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Install WebDriver

**Chrome:**
- Install Chrome browser
- Or use webdriver-manager (installed via requirements.txt)

**Firefox:**
- Install Firefox browser
- Geckodriver should be automatically managed

### 3. Run Locally

```bash
# Run with Chrome (default, headless)
python scraper.py

# Run with Firefox
python scraper.py --browser firefox

# Run with visible browser (not headless)
python scraper.py --no-headless

# Specify custom output directory
python scraper.py --output /path/to/output
```

## Running with Podman

### 1. Build the Container

```bash
podman build -t gadm-downloader .
```

### 2. Run the Container

```bash
# Run with Chrome (default)
podman run --rm -v $(pwd)/downloads:/app/downloads gadm-downloader

# Run with Firefox
podman run --rm -v $(pwd)/downloads:/app/downloads gadm-downloader python scraper.py --browser firefox

# Run with visible browser (for debugging)
podman run --rm -v $(pwd)/downloads:/app/downloads gadm-downloader python scraper.py --no-headless
```

### 3. Volume Mount

The container mounts the `downloads` directory to persist downloaded files:
- Host: `./downloads`
- Container: `/app/downloads`

## Project Structure

```
get-un-admin-boundaries/
├── scraper.py          # Main Python application
├── Containerfile       # Podman container definition
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── downloads/         # Downloaded GeoJSON files (created at runtime)
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--browser` | Browser to use (chrome/firefox) | chrome |
| `--no-headless` | Run browser in visible mode | headless |
| `--output` | Output directory for downloads | downloads |

## Notes

- The script is polite to the server by adding delays between downloads
- Downloaded files are saved to the `downloads` directory
- GeoJSON files are typically named like `gadm41_XXX_geojson.zip`
- Some countries have multiple levels (0-4) of administrative boundaries