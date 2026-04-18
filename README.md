# GADM GeoJSON Downloader

A Python web scraping application wrapped in a docker container that downloads GeoJSON administrative boundary files from [GADM](https://gadm.org).

## Initializing repo

- Create directories for "output" and "logs": ```mkdir output logs```

## Docker commands or Docker Compose commands

### Docker
- Build: ```docker build -t gadm-downloader .```
- Run options:
    - Run with default command (currently does nothing): ```docker run --rm gadm-downloader```

    - Run with debug logging: ```docker run --rm -e LOG_LEVEL=DEBUG gadm-downloader```

    - Run with volume mount for output files: ```docker run --rm -v $(pwd)/output:/app/output -v $(pwd)/logs:/app/logs gadm-downloader```

    - Run python app command interactively (enter container shell): ```docker run --rm -it -v $(pwd)/output:/app/output -v $(pwd)/logs:/app/logs gadm-downloader python app.py --help```
    
    - Run interactively (enter container shell): ```docker run --rm -it gadm-downloader /bin/sh```

    - Run with all options interactively (debug + volumes + interactive): ```docker run --rm -it -e LOG_LEVEL=DEBUG -v $(pwd)/output:/app/output -v $(pwd)/logs:/app/logs gadm-downloader /bin/sh```

    - Run with all options command prompt (debug + volumes): ```docker run --rm -e LOG_LEVEL=DEBUG -v $(pwd)/output:/app/output -v $(pwd)/logs:/app/logs gadm-downloader python app.py --help```

### Docker Compose

The [docker-compose.yaml](./docker-compose.yaml) file is configured with the most common use case. During development edit the ```command``` variable for testing needs. If needs get more specific it is recommended to use the **_Docker_** commands above. Otherwise use the command ```docker compose up --build``` to execute the yaml file