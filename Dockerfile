# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed
# (uncomment if BeautifulSoup or networking needs system libs later)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy full application (NOT just app.py anymore)
COPY . .

# Ensure runtime directories exist
RUN mkdir -p /app/output /app/logs

# Optional: make Python output cleaner in Docker logs
ENV PYTHONUNBUFFERED=1

# Default command now points to your CLI entrypoint
CMD ["python", "/app/main.py"]