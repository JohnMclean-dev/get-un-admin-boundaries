FROM ghcr.io/osgeo/gdal:ubuntu-small-latest

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Create and use venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/output /app/logs

ENV PYTHONUNBUFFERED=1

CMD ["python", "/app/gadm_downloader/main.py"]