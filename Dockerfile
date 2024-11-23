FROM python:3.11-slim-buster

# Add build argument for cache busting
ARG CACHE_BUST=1

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

# Copy requirements with cache busting
COPY ./requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Cache bust for project files
COPY --chown=app:app . .

# Alternative: Copy individual directories with cache busting
ARG FILES_CACHE_BUST=1
COPY ./credentials.json ${APP_HOME}/
COPY ./app/ ${APP_HOME}/app/
COPY ./static/ ${APP_HOME}/static/
COPY ./worker/ ${APP_HOME}/worker/
COPY ./run.sh ${APP_HOME}/

ENTRYPOINT [ "sh", "run.sh" ]