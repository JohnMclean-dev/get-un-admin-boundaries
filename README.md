# GADM GeoJSON Downloader

A Python web scraping application wrapped in a Podman container that downloads GeoJSON administrative boundary files from [GADM](https://gadm.org).

## Initializing repo

- Create directories for "output" and "logs": ```mkdir output logs```

## Podman commands

- Build: ```podman build -t gadm-downloader .```
- Run options:
    - Run with default command (currently does nothing): ```podman run --rm gadm-downloader```

    - Run with debug logging: ```podman run --rm -e LOG_LEVEL=DEBUG gadm-downloader```

    - Run with volume mount for output files: ```podman run --rm -v $(pwd)/output:/app/output -v $(pwd)/logs:/app/logs gadm-downloader```

    - Run python app command interactively (enter container shell): ```podman run --rm -it -v $(pwd)/output:/app/output -v $(pwd)/logs:/app/logs gadm-downloader python app.py --help```
    
    - Run interactively (enter container shell): ```podman run --rm -it gadm-downloader /bin/sh```

    - Run with all options interactively (debug + volumes + interactive): ```podman run --rm -it -e LOG_LEVEL=DEBUG -v $(pwd)/output:/app/output -v $(pwd)/logs:/app/logs gadm-downloader /bin/sh```

    - Run with all options command prompt (debug + volumes): ```podman run --rm -e LOG_LEVEL=DEBUG -v $(pwd)/output:/app/output -v $(pwd)/logs:/app/logs gadm-downloader python app.py --help```
