# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for GeoPandas / GDAL stack
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    proj-data \
    proj-bin \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Ensure GDAL can be found during pip installs
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Copy requirements first (better caching)
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy full application
COPY . .

# Ensure runtime directories exist
RUN mkdir -p /app/output /app/logs

# Cleaner logs in Docker
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "/app/gadm_downloader/main.py"]