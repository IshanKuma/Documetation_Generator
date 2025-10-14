# ==========================================
# Documentation Generator - Docker Image
# ==========================================
# Multi-stage build for optimized image size
# Base: Python 3.13 with Chromium for screenshots

FROM python:3.13-slim

# Metadata
LABEL maintainer="Documentation Generator"
LABEL description="AI-powered documentation generator with screenshot capabilities"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for Chrome/Chromium, screenshots, and diagram generation
# Why these packages:
# - chromium: Headless browser for screenshots (lighter than full Chrome)
# - chromium-driver: Selenium WebDriver for Chromium
# - fonts-liberation: Better font rendering in screenshots
# - nodejs, npm: Required for mermaid-cli diagram rendering
# - libreoffice-writer: For PDF export on Linux
# - wget, gnupg: For package management
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    fonts-liberation \
    fonts-dejavu-core \
    nodejs \
    npm \
    libreoffice-writer \
    libreoffice-java-common \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Mermaid CLI for diagram rendering
# Why: Enables generation of architecture diagrams from text-based Mermaid code
RUN npm install -g @mermaid-js/mermaid-cli

# Set Chromium path for Selenium
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Create app directory
WORKDIR /app

# Copy requirements first (Docker layer caching optimization)
# If requirements don't change, this layer is cached
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY doc_generator.py .
COPY run_doc_generator.py .

# Create directories for output, screenshots, and mermaid diagrams
RUN mkdir -p /app/output /app/screenshots /app/mermaid_diagrams

# Create non-root user for security
# Running as root in containers is a security risk
RUN useradd -m -u 1000 docgen && \
    chown -R docgen:docgen /app

# Switch to non-root user
USER docgen

# Volume mounts (defined in docker-compose.yml):
# - /app/output: Generated documentation
# - /app/screenshots: Captured screenshots
# - /app/project: Source code to document (mounted from host)

# Default command
CMD ["python", "doc_generator.py"]
