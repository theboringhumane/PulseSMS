FROM python:3.11-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_HOME=/app

# Set working directory
WORKDIR ${APP_HOME}

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
# COPY credentials.json ${APP_HOME}/
COPY app/ ${APP_HOME}/app/
COPY static/ ${APP_HOME}/static/
COPY worker/ ${APP_HOME}/worker/