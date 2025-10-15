# ==========================================
# Documentation Generator - Docker Image
# Version: 1.2.2
# ==========================================
# Multi-stage build for optimized image size
# Base: Python 3.13 with Chromium for screenshots

FROM python:3.13-slim

# Metadata
LABEL maintainer="Documentation Generator"
LABEL description="Autonomous AI documentation generator - no interaction required"
LABEL version="1.2.2"
LABEL release-date="2025-10-15"
LABEL features="Autonomous operation, URL health checks, Smart repomix resolution, Rate limiting"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for Chrome/Chromium, screenshots, and diagram generation
# Why these packages:
# - chromium + chromium-driver: Browser and driver (matched versions from same repo)
# - fonts-liberation: Better font rendering in screenshots
# - nodejs, npm: Required for mermaid-cli diagram rendering
# - libreoffice-writer: For PDF export on Linux
# - wget, gnupg: For package management
#
# CRITICAL FIX: Install BOTH chromium AND chromium-driver from apt
# This ensures they are from the same repository and have matching versions
# Avoids "ChromeDriver only supports Chrome version X" errors
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

# Set Chromium and ChromeDriver paths for Selenium + Puppeteer
# CRITICAL: Point Selenium to system-installed ChromeDriver (not webdriver-manager)
# This ensures version compatibility since both come from same apt repository
# PUPPETEER_EXECUTABLE_PATH: Configure puppeteer (used by mmdc) to use Chromium
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

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
# Note: These will be overridden by volume mounts, but we create them for non-Docker runs
RUN mkdir -p /app/output /app/screenshots /app/mermaid_diagrams

# Create non-root user for security
# Running as root in containers is a security risk
RUN useradd -m -u 1000 docgen && \
    chown -R docgen:docgen /app

# Create entrypoint script to fix volume permissions
# This script runs before the main application and ensures mounted volumes are writable
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Switch to non-root user
USER docgen

# Volume mounts (defined in docker-compose.yml):
# - /app/output: Generated documentation
# - /app/screenshots: Captured screenshots
# - /app/project: Source code to document (mounted from host)

# Default entrypoint: Fix permissions then run app
# Entrypoint runs first, CMD runs after
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Default command: Use wrapper script for better error handling
# and completion detection (creates .complete marker file)
CMD ["python", "run_doc_generator.py"]
