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

The application uses **explicit modes** for file handling and database operations.

---

### File Handling Modes

```bash
--file-mode {skip,overwrite,refresh}
```

| Mode        | Behavior |
|------------|--------|
| skip (default) | Skip existing files |
| overwrite | Re-download and overwrite existing files |
| refresh | Delete all files in `output/` before downloading |

---

### Database Modes (planned)

```bash
--db-mode {create-if-new,append,truncate,check-if-exists}
```

| Mode | Behavior |
|------|--------|
| create-if-new (default) | Create tables if they do not exist, then insert data |
| append | Insert data into existing tables |
| truncate | Clear tables, then insert data |
| check-if-exists | Verify required tables exist (no data written) |

> ⚠️ Database functionality is **not yet implemented**.  
> These modes define intended behavior for upcoming Postgres/PostGIS integration.

---

## 🐳 Docker Usage

### Build Image

```bash
docker build -t gadm-downloader .
```

---

### Run (Default)

```bash
docker run --rm gadm-downloader
```

---

### Run with Debug Logging

```bash
docker run --rm -e LOG_LEVEL=DEBUG gadm-downloader
```

---

### Run with Data Persistence (Volumes)

```bash
docker run --rm \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  gadm-downloader
```

---

### Run with Custom CLI Options

```bash
docker run --rm \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  gadm-downloader \
  python gadm_downloader/main.py --file-mode overwrite --db-mode create-if-new
```

---

### Interactive Mode

```bash
docker run --rm -it gadm-downloader /bin/sh
```

---

### CLI Help

```bash
docker run --rm gadm-downloader python gadm_downloader/main.py --help
```

---

## 🐳 Docker Compose

### Production / Default

Run the standard pipeline:

```bash
docker compose up --build
```

---

### Select Environment

Run the application in different environments using Compose overrides:

#### Development (mounted source code, debug-friendly)
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

#### Staging
```bash
docker compose -f docker-compose.yml -f docker-compose.stg.yml up --build
```

#### Production
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

---

## 🚀 Pipeline Overview

1. Scrape GADM download page  
2. Download dataset archives  
3. Extract archives  
4. Discover GeoPackage files  
5. Load into a GeoDataFrame  
6. *(Planned)* Load into Postgres/PostGIS  

---

## 🔮 Future Enhancements

- Postgres/PostGIS integration
- Automated schema creation & validation
