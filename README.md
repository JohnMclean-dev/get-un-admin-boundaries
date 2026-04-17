# GADM GeoJSON Downloader

A Python web scraping application wrapped in a Podman container that downloads GeoJSON administrative boundary files from [GADM](https://gadm.org).

## Podman commands

- Build: ```podman build -t gadm-downloader .```
- Run options:
    - Run with default command (currently does nothing): ```podman run --rm gadm-downloader```

    - Run with volume mount for output files: ```podman run --rm -v $(pwd)/output:/app/output gadm-downloader```

    - Run interactively (enter the container shell): ```podman run --rm -it gadm-downloader /bin/sh```

    - Run with custom arguments (once you add argparse): ```podman run --rm -v $(pwd)/output:/app/output gadm-downloader --country USA --level 1```
