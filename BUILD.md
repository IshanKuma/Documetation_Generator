# Building and Deploying Version 1.2

This guide covers building and deploying the Documentation Generator Docker container version 1.2.

## Quick Start

### Build the Image

```bash
# Build with version 1.2 tag
docker-compose build

# Or build directly with Docker
docker build -t documentation_generator:1.2 .
```

### Run the Container

```bash
# Run using docker-compose (recommended)
docker-compose up

# Or run directly with Docker
docker run --rm \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/screenshots:/app/screenshots \
  -v $(pwd)/mermaid_diagrams:/app/mermaid_diagrams \
  -v /path/to/project:/app/project \
  -e GEMINI_API_KEY=your_api_key_here \
  -e PROJECT_NAME="Your Project" \
  -e PROJECT_PATH=/app/project \
  documentation_generator:1.2
```

## Version 1.2 Features

### What's New
- **Intelligent Rate Limiting**: Prevents API quota exhaustion
- **Content Optimization**: Flexible section count (9-15)
- **Screenshot Limits**: Max 8 screenshots per document
- **Diagram Limits**: Max 3 mermaid diagrams
- **Better Docker Lifecycle**: No more restart loops

### Breaking Changes
- Default `GEMINI_REQUEST_DELAY` changed from 2s to 5s
- New required environment variables (all have defaults)

## Deployment to Another System

### Prerequisites
1. Docker and Docker Compose installed
2. Google Gemini API key

### Steps

1. **Copy the project directory** to the target system:
```bash
# Exclude unnecessary files
rsync -av --exclude='.git' --exclude='output' --exclude='screenshots' \
  --exclude='*.tar.gz' --exclude='venv' \
  /path/to/documentation_generator/ \
  user@target:/path/to/destination/
```

2. **Edit docker-compose.yml** on the target system:
   - Set `GEMINI_API_KEY`
   - Set `PROJECT_NAME`
   - Update volume mount for `PROJECT_PATH`

3. **Build the image**:
```bash
docker-compose build
```

4. **Run the generator**:
```bash
docker-compose up
```

5. **Check completion**:
```bash
# Container will stop when done
# Check exit code
docker-compose ps

# View output
ls -la output/
```

## Docker Hub Deployment (Optional)

### Tag and Push

```bash
# Login to Docker Hub
docker login

# Tag the image
docker tag documentation_generator:1.2 yourusername/documentation_generator:1.2
docker tag documentation_generator:1.2 yourusername/documentation_generator:latest

# Push to Docker Hub
docker push yourusername/documentation_generator:1.2
docker push yourusername/documentation_generator:latest
```

### Pull and Run on Another System

```bash
# Pull from Docker Hub
docker pull yourusername/documentation_generator:1.2

# Run
docker run --rm \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/screenshots:/app/screenshots \
  -v $(pwd)/mermaid_diagrams:/app/mermaid_diagrams \
  -v /path/to/project:/app/project \
  -e GEMINI_API_KEY=your_api_key_here \
  -e PROJECT_NAME="Your Project" \
  -e PROJECT_PATH=/app/project \
  yourusername/documentation_generator:1.2
```

## Environment Variables Reference

### Required
- `GEMINI_API_KEY`: Your Google Gemini API key
- `PROJECT_NAME`: Name of your project
- `PROJECT_PATH`: Path to project directory (in container)

### Rate Limiting (New in 1.2)
- `GEMINI_REQUEST_DELAY=5`: Default delay between requests
- `GEMINI_PLAN_REQUEST_DELAY=5`: Delay for plan generation
- `GEMINI_SECTION_REQUEST_DELAY=5`: Delay for section generation
- `GEMINI_SCREENSHOT_REQUEST_DELAY=5`: Delay for screenshot analysis
- `GEMINI_DIAGRAM_REQUEST_DELAY=5`: Delay for diagram generation
- `GEMINI_MAX_REQUESTS_PER_MINUTE=15`: Rate limit enforcement
- `GEMINI_MAX_RETRIES=3`: Retry attempts on failure
- `GEMINI_BASE_BACKOFF_DELAY=5`: Exponential backoff base delay

### Optimization (New in 1.2)
- `MIN_SECTIONS=9`: Minimum sections to generate
- `MAX_SECTIONS=15`: Maximum sections to generate
- `MAX_SCREENSHOTS_PER_DOCUMENT=8`: Screenshot limit
- `MAX_MERMAID_DIAGRAMS=3`: Diagram limit
- `SCREENSHOT_PRIORITY_SECTIONS`: Comma-separated priority sections

## Troubleshooting

### Container Exits Immediately
```bash
# Check logs
docker-compose logs

# Common issues:
# - Invalid GEMINI_API_KEY
# - Missing volume mounts
# - Permission errors
```

### Rate Limit Errors
```bash
# Increase delay in docker-compose.yml
GEMINI_REQUEST_DELAY=7  # Slower but safer
```

### Out of Memory
```bash
# Add resource limits in docker-compose.yml (uncomment deploy section)
deploy:
  resources:
    limits:
      memory: 4G
```

## Verification

### Check Image Info
```bash
# View image metadata
docker inspect documentation_generator:1.2

# Check version label
docker inspect --format='{{.Config.Labels.version}}' documentation_generator:1.2
```

### Test Run
```bash
# Test with this project itself
docker-compose up

# Expected output:
# - Documentation generation progress
# - Screenshots captured
# - Diagrams generated
# - Container exits with code 0
# - Files in output/
```

## Rollback to Previous Version

```bash
# If you have version 1.0 or 1.1
docker-compose down
docker tag documentation_generator:1.0 documentation_generator:latest
docker-compose up
```

## Support

For issues or questions:
- Check CHANGELOG.md for known issues
- Review docker-compose.yml comments
- Verify environment variables
- Check Docker logs
