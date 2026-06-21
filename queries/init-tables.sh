#!/usr/bin/env bash

set -euo pipefail

# ---- configuration ----
PROJECT_DIR="/home/dijon/Documents/get-un-admin-boundaries"
LOG_FILE="$PROJECT_DIR/queries/logs/create-tables_$(date +%Y-%m-%d_%H-%M-%S).log"

mkdir -p "$PROJECT_DIR/queries/logs"
# rm "$PROJECT_DIR/queries/logs/create-tables_*.log"

# Send all stdout/stderr to both console and log file
exec > >(tee -a "$LOG_FILE") 2>&1

echo "=============================="
echo "Starting run: $(date)"
echo "Log file: $LOG_FILE"
echo "=============================="

cd "$PROJECT_DIR"

echo "[1/9] Stopping existing containers..."
echo "Skipping..."
# docker compose -f docker-compose.yml -f docker-compose.dev.yml down

echo "[2/9] Building and starting containers..."
echo "Skipping..."
# docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

echo "[3/9] Verifying administrative boundary data..."
echo "Skipping..."
# docker exec -it gadm-downloader sh -c "python /app/gadm_downloader/main.py --file-mode skip --db-mode check-if-exists"

echo "[4/9] Cleaning up downloader container and system resources..."
echo "Skipping..."
# docker stop gadm-downloader
# docker rm gadm-downloader
# docker system prune

echo "[5/9] Preparing PostgreSQL container workspace..."
# echo "Skipping..."
docker exec postgres sh -c "rm -rf /tmp/create-tables/"

echo "[6/9] Copying CSV data into container..."
# echo "Skipping..."
docker cp "$(pwd)/world-cities-data/simplemaps_worldcities_basicv1.91/worldcities.csv" postgres:/tmp/worldcities.csv

echo "[7/9] Copying SQL scripts into container..."
# echo "Skipping..."
docker cp "$(pwd)/queries/create-tables" postgres:/tmp/

run_sql () {
  local file="$1"
  echo "Running $file ..."
  docker exec postgres \
    psql -U gadm_user -d gadm -f "/tmp/create-tables/$file"
}

echo "[8/9] Executing table creation and lookup scripts..."
# echo "Skipping..."

run_sql "worldcities.sql"

docker exec postgres \
    psql -U gadm_user -d gadm -c \
    "\copy public.worldcities(city, city_ascii, lat, lng, country, iso2, iso3, admin_name, capital, population, id) FROM '/tmp/worldcities.csv' WITH (FORMAT csv, HEADER true);"

run_sql "cities-init.sql"
run_sql "continents.sql"
# run_sql "cities-continents-lkp.sql"
run_sql "districts.sql"
# run_sql "cities-districts-lkp.sql"
run_sql "regions.sql"
run_sql "countries.sql"

echo "[9/9] Running final schema inspection..."
# echo "Skipping..."
docker exec postgres psql -U gadm_user -d gadm -c "\d"

echo
echo "=============================="
echo "Completed successfully: $(date)"
echo "=============================="