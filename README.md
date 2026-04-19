# GADM GeoJSON Downloader

A Python web scraping application wrapped in a Docker container that downloads GeoJSON/GeoPackage administrative boundary files from [GADM](https://gadm.org).

---

## 📦 Initialization

Create required directories:

```bash
mkdir output logs
```

---

## ⚙️ CLI Options

The application uses **explicit modes** for file handling and (future) database operations.

### File Handling Modes

```bash
--file-mode {skip,overwrite,refresh}
```

| Mode        | Behavior |
|------------|--------|
| skip (default) | Skip existing files |
| overwrite | Re-download and overwrite existing files |
| refresh | Delete all files in output/ before downloading |

---

### Database Modes (future use)

```bash
--db-mode {append,truncate}
```

| Mode       | Behavior |
|-----------|--------|
| append (default) | Add data to existing table |
| truncate | Clear table before inserting |

> ⚠️ Database functionality is not yet implemented.

---

## 🐳 Docker Usage

### Build Image

```bash
docker build -t gadm-downloader .
```

---

### Run Examples

#### Default run

```bash
docker run --rm gadm-downloader
```

---

#### Debug logging

```bash
docker run --rm -e LOG_LEVEL=DEBUG gadm-downloader
```

---

#### With volumes

```bash
docker run --rm \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  gadm-downloader
```

---

#### CLI option example

```bash
docker run --rm \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  gadm-downloader \
  python gadm_downloader/main.py --file-mode overwrite
```

---

#### Full refresh

```bash
docker run --rm \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  gadm-downloader \
  python gadm_downloader/main.py --file-mode refresh
```

---

#### Interactive shell

```bash
docker run --rm -it gadm-downloader /bin/sh
```

---

#### Debug + interactive

```bash
docker run --rm -it \
  -e LOG_LEVEL=DEBUG \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  gadm-downloader /bin/sh
```

---

#### CLI help

```bash
docker run --rm gadm-downloader python gadm_downloader/main.py --help
```

---

## 🐳 Docker Compose

```bash
docker compose up --build
```

---

## 🚀 Pipeline Overview

1. Scrape GADM download page  
2. Download dataset archives  
3. Extract archives  
4. Discover GeoPackage files  
5. Load into a GeoDataFrame  

---

## 🔮 Future Enhancements

- Postgres/PostGIS integration
