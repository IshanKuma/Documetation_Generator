# Docker Setup Guide
## Documentation Generator - Container Distribution

---

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Configuration](#configuration)
5. [Running the Container](#running-the-container)
6. [Volume Mounts Explained](#volume-mounts-explained)
7. [Common Use Cases](#common-use-cases)
8. [Testing on Different Projects](#testing-on-different-projects)
9. [Troubleshooting](#troubleshooting)
10. [Platform-Specific Notes](#platform-specific-notes)

---

## Overview

This Docker setup allows you to run the Documentation Generator on any system without installing Python, Selenium, or other dependencies locally. Perfect for:

- Testing the generator on different projects (UI, ML, backend, etc.)
- Distributing to team members who don't have Python installed
- Running in CI/CD pipelines
- Ensuring consistent behavior across different systems

**What's included:**
- Python 3.13 runtime
- Chromium browser (for screenshots)
- All Python dependencies pre-installed
- Non-root user for security

---

## Prerequisites

### Required Software
- **Docker Desktop** (includes Docker Engine + Docker Compose)
  - Windows: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
  - macOS: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
  - Linux: Install Docker Engine + Docker Compose
    ```bash
    # Ubuntu/Debian
    sudo apt update
    sudo apt install docker.io docker-compose
    sudo systemctl start docker
    sudo systemctl enable docker

    # Add your user to docker group (no sudo needed)
    sudo usermod -aG docker $USER
    newgrp docker
    ```

### Verify Installation
```bash
# Check Docker version
docker --version
# Should show: Docker version 20.x.x or higher

# Check Docker Compose version
docker-compose --version
# Should show: docker-compose version 1.29.x or higher
```

### Required: Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (you'll need it in the next step)

---

## Quick Start

### 1. Clone or Copy the Project
```bash
# If using git
git clone <repository-url>
cd documentation_generator

# Or download and extract ZIP, then navigate to folder
```

### 2. Configure Environment Variables

Open `docker-compose.yml` and edit these essential variables:

```yaml
environment:
  # REQUIRED: Your Gemini API key
  - GEMINI_API_KEY=AIza...your_actual_key_here

  # REQUIRED: Project information
  - PROJECT_NAME=My Awesome Project
  - PROJECT_DESCRIPTION=A brief description of what this project does
```

### 3. Build the Docker Image
```bash
# Build the image (first time only, takes 2-5 minutes)
docker-compose build

# Or build without cache (if you made changes)
docker-compose build --no-cache
```

### 4. Run the Container
```bash
# Run the documentation generator
docker-compose up

# Or run in detached mode (background)
docker-compose up -d

# View logs if running in background
docker-compose logs -f
```

### 5. Find Your Documentation
After the container finishes (usually 2-10 minutes depending on project size):

```bash
# Documentation will be in:
./output/documentation.docx

# Screenshots will be in:
./screenshots/
```

---

## Configuration

### Essential Environment Variables

Edit these in `docker-compose.yml` under `environment:` section:

#### Google Gemini API
```yaml
- GEMINI_API_KEY=your_api_key_here        # REQUIRED: Your API key
- GEMINI_MODEL=gemini-2.5-pro              # Model to use (or gemini-2.0-flash-exp)
- GEMINI_TEMPERATURE=0.7                   # Creativity (0.0-1.0, higher = more creative)
```

#### Project Configuration
```yaml
- PROJECT_NAME=Your Project Name           # REQUIRED: Project name for docs
- PROJECT_PATH=/app/project                # Don't change (internal container path)
- PROJECT_DESCRIPTION=Brief description    # Optional but recommended
```

#### Screenshot Settings
```yaml
- ENABLE_SCREENSHOTS=true                  # true/false - capture code screenshots
- BROWSER_CHOICE=chrome                    # chrome or firefox (chrome recommended)
- SCREENSHOT_WAIT_TIME=3                   # Seconds to wait before screenshot
```

#### Documentation Sections
```yaml
- INCLUDE_OVERVIEW=true                    # Include overview section
- INCLUDE_ARCHITECTURE=true                # Include architecture diagrams
- INCLUDE_INSTALLATION=true                # Include setup instructions
- INCLUDE_API_REFERENCE=true               # Include API documentation
- INCLUDE_TROUBLESHOOTING=true             # Include troubleshooting section
```

### Advanced Configuration

#### Live App Screenshots (For UI Projects)
If you're documenting a web app and want to capture running app screenshots:

```yaml
- LIVE_APP_ENABLED=true                    # Enable live app screenshots
- LIVE_APP_URL_HOME=http://host.docker.internal:3000
- LIVE_APP_URL_DASHBOARD=http://host.docker.internal:3000/dashboard
```

**Note:** `host.docker.internal` allows the container to access services running on your host machine.

#### Repomix Integration (Better AI Context)
For larger projects, use [repomix](https://github.com/yamadashy/repomix) to create a comprehensive context file:

```bash
# Install repomix (if not installed)
npm install -g repomix

# Generate repomix file for your project
repomix /path/to/your/project -o repomix-output.xml

# Place repomix-output.xml in your project directory

# Enable in docker-compose.yml
- USE_REPOMIX=true
- REPOMIX_FILE_PATH=/app/project/repomix-output.xml
```

#### Excluded Directories
Customize which directories to ignore:

```yaml
- EXCLUDED_DIRECTORIES=node_modules,.git,__pycache__,venv,.venv,dist,build,target
```

---

## Running the Container

### Basic Run
```bash
# Build and run
docker-compose up

# Run in background
docker-compose up -d

# Stop container
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### View Logs
```bash
# Follow logs in real-time
docker-compose logs -f

# Show last 100 lines
docker-compose logs --tail=100
```

### Rebuild After Changes
```bash
# Rebuild image after modifying Dockerfile
docker-compose build

# Rebuild and restart
docker-compose up --build
```

### Execute Commands in Container
```bash
# Open shell in container
docker-compose exec doc-generator bash

# Run Python interactively
docker-compose exec doc-generator python

# Check Python version
docker-compose exec doc-generator python --version
```

---

## Volume Mounts Explained

Volumes connect directories on your host machine to the container:

```yaml
volumes:
  - ./output:/app/output              # Generated docs go here
  - ./screenshots:/app/screenshots    # Screenshots saved here
  - .:/app/project                    # Project to document
```

### Custom Project Path

To document a different project (not this tool itself):

**Linux/macOS:**
```yaml
volumes:
  - ./output:/app/output
  - ./screenshots:/app/screenshots
  - /home/user/myproject:/app/project              # Absolute path
  - ~/code/another-project:/app/project            # Relative to home
```

**Windows:**
```yaml
volumes:
  - ./output:/app/output
  - ./screenshots:/app/screenshots
  - C:/Users/YourName/Projects/myapp:/app/project  # Windows path
```

---

## Common Use Cases

### Use Case 1: Document This Tool (Self-Documentation)
```yaml
# In docker-compose.yml
environment:
  - PROJECT_NAME=Documentation Generator
  - PROJECT_DESCRIPTION=AI-powered documentation generator

volumes:
  - .:/app/project  # Current directory
```

```bash
docker-compose up
```

### Use Case 2: Document a Python/ML Project
```yaml
# In docker-compose.yml
environment:
  - PROJECT_NAME=My ML Model
  - PROJECT_DESCRIPTION=Machine learning model for image classification
  - INCLUDE_API_REFERENCE=true
  - INCLUDE_DEPLOYMENT=true

volumes:
  - /path/to/ml-project:/app/project
```

### Use Case 3: Document a React/UI Project
```yaml
# In docker-compose.yml
environment:
  - PROJECT_NAME=My React App
  - PROJECT_DESCRIPTION=Modern web application with React
  - LIVE_APP_ENABLED=true
  - LIVE_APP_URL_HOME=http://host.docker.internal:3000
  - LIVE_APP_URL_DASHBOARD=http://host.docker.internal:3000/dashboard

volumes:
  - /path/to/react-app:/app/project
```

**Important:** Start your React app first:
```bash
# In another terminal
cd /path/to/react-app
npm start

# Then run the documentation generator
docker-compose up
```

### Use Case 4: Document a REST API Project
```yaml
# In docker-compose.yml
environment:
  - PROJECT_NAME=My REST API
  - PROJECT_DESCRIPTION=RESTful API for managing resources
  - INCLUDE_API_REFERENCE=true
  - LIVE_APP_ENABLED=true
  - LIVE_APP_URL_API_DOCS=http://host.docker.internal:8000/docs

volumes:
  - /path/to/api-project:/app/project
```

### Use Case 5: Batch Documentation for Multiple Projects
```bash
# Create a script to document multiple projects
#!/bin/bash

PROJECTS=(
  "/home/user/project1:Project One:Python backend service"
  "/home/user/project2:Project Two:React frontend"
  "/home/user/project3:Project Three:ML model"
)

for project_info in "${PROJECTS[@]}"; do
  IFS=':' read -r path name desc <<< "$project_info"

  echo "Documenting: $name"

  # Update docker-compose.yml
  sed -i "s|PROJECT_NAME=.*|PROJECT_NAME=$name|" docker-compose.yml
  sed -i "s|PROJECT_DESCRIPTION=.*|PROJECT_DESCRIPTION=$desc|" docker-compose.yml

  # Update volume mount
  # (Or create separate docker-compose files)

  # Run
  docker-compose up

  # Rename output
  mv output/documentation.docx "output/${name// /_}_docs.docx"
done
```

---

## Testing on Different Projects

### Step-by-Step: Test on a New Project

1. **Choose a project to document**
   ```bash
   ls /path/to/your/projects
   ```

2. **Update docker-compose.yml**
   ```yaml
   environment:
     - PROJECT_NAME=Your Project Name
     - PROJECT_DESCRIPTION=Description of the project

   volumes:
     - /absolute/path/to/project:/app/project
   ```

3. **Optional: Generate repomix for better context**
   ```bash
   cd /path/to/project
   repomix . -o repomix-output.xml
   ```

4. **Run the generator**
   ```bash
   cd /path/to/documentation_generator
   docker-compose up
   ```

5. **Review output**
   ```bash
   # Documentation
   ls -lh output/documentation.docx

   # Screenshots
   ls screenshots/

   # Open documentation
   # Linux
   xdg-open output/documentation.docx

   # macOS
   open output/documentation.docx

   # Windows
   start output/documentation.docx
   ```

### Quality Check for Different Project Types

#### Python/Backend Projects
- Check if architecture diagrams are accurate
- Verify API endpoints are documented
- Ensure code examples are relevant
- Review setup instructions

#### UI/Frontend Projects
- Verify component structure is documented
- Check if screenshots captured UI properly
- Ensure routing is explained
- Review state management documentation

#### ML/Data Science Projects
- Check if model architecture is explained
- Verify data preprocessing steps
- Ensure training process is documented
- Review performance metrics section

---

## Troubleshooting

### Problem: "docker: command not found"
**Solution:** Docker is not installed or not in PATH
```bash
# Verify installation
which docker

# Linux: Install Docker
sudo apt install docker.io

# macOS/Windows: Install Docker Desktop
# https://www.docker.com/products/docker-desktop
```

### Problem: "permission denied while trying to connect to Docker daemon"
**Solution:** User not in docker group (Linux)
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login, or run:
newgrp docker

# Verify
docker ps
```

### Problem: "build failed" or "cannot find Dockerfile"
**Solution:** Ensure you're in the correct directory
```bash
# Check current directory
pwd

# Should contain Dockerfile
ls -la Dockerfile

# Navigate to project directory
cd /path/to/documentation_generator
```

### Problem: "Gemini API error" or "API key not found"
**Solution:** Check your API key configuration
```bash
# Verify API key in docker-compose.yml
grep GEMINI_API_KEY docker-compose.yml

# Should not be empty or placeholder
# GEMINI_API_KEY=AIza... (starts with AIza)

# Test API key validity
curl -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
  "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-pro:generateContent?key=YOUR_API_KEY"
```

### Problem: "No screenshots generated"
**Solution:** Check screenshot configuration
```yaml
# In docker-compose.yml
- ENABLE_SCREENSHOTS=true
- BROWSER_CHOICE=chrome
```

```bash
# Check if Chromium is installed in container
docker-compose exec doc-generator which chromium

# View logs for screenshot errors
docker-compose logs | grep -i screenshot
```

### Problem: "Container exits immediately"
**Solution:** Check logs for errors
```bash
# View logs
docker-compose logs

# Common errors:
# - Missing environment variables
# - Invalid project path
# - Gemini API quota exceeded
```

### Problem: "Cannot access host machine's localhost"
**Solution:** Use `host.docker.internal` instead of `localhost`
```yaml
# Wrong
- LIVE_APP_URL_HOME=http://localhost:3000

# Correct
- LIVE_APP_URL_HOME=http://host.docker.internal:3000
```

### Problem: "Documentation quality is poor"
**Solutions:**
1. **Use repomix for better context**
   ```bash
   repomix /path/to/project -o repomix-output.xml
   ```

2. **Adjust Gemini settings**
   ```yaml
   - GEMINI_MODEL=gemini-2.5-pro  # Better quality than flash
   - GEMINI_TEMPERATURE=0.5       # Lower = more focused
   ```

3. **Enable more sections**
   ```yaml
   - INCLUDE_ARCHITECTURE=true
   - INCLUDE_API_REFERENCE=true
   - INCLUDE_DEVELOPMENT_GUIDE=true
   ```

### Problem: "Build takes too long"
**Solution:** Docker may be downloading layers
```bash
# First build takes 2-5 minutes (normal)
# Subsequent builds should be faster (cached)

# Clean build if needed
docker-compose build --no-cache

# Check disk space
df -h
```

### Problem: "Out of disk space"
**Solution:** Clean up Docker resources
```bash
# Remove unused containers
docker container prune

# Remove unused images
docker image prune

# Remove everything (careful!)
docker system prune -a

# Check Docker disk usage
docker system df
```

---

## Platform-Specific Notes

### Windows

#### File Paths
- Use forward slashes or escape backslashes in docker-compose.yml
  ```yaml
  # Good
  - C:/Users/YourName/Project:/app/project

  # Also works
  - C:\\Users\\YourName\\Project:/app/project
  ```

#### Line Endings
- Ensure files use LF (not CRLF) line endings
  ```bash
  # In git
  git config core.autocrlf false
  ```

#### Performance
- Docker Desktop on Windows uses WSL2 for better performance
- Store projects in WSL2 filesystem for faster builds
  ```bash
  # Access WSL2 from Windows
  \\wsl$\Ubuntu\home\user\project
  ```

### macOS

#### Docker Desktop Memory
- Allocate sufficient memory in Docker Desktop settings
- Recommended: 4GB minimum, 8GB for large projects

#### File Permissions
- macOS paths are case-sensitive
- Ensure volume mount paths are correct

### Linux

#### SELinux (Fedora/RHEL)
- Add `:z` suffix to volume mounts if using SELinux
  ```yaml
  volumes:
    - ./output:/app/output:z
    - ./screenshots:/app/screenshots:z
  ```

#### User Permissions
- Container runs as user `docgen` (UID 1000)
- Ensure host directories are writable
  ```bash
  # Fix permissions if needed
  sudo chown -R 1000:1000 output screenshots
  ```

---

## Next Steps

1. **Test on sample project**
   - Start with a small, simple project
   - Review the generated documentation
   - Adjust settings as needed

2. **Customize for your needs**
   - Add project-specific exclusions to .dockerignore
   - Adjust documentation sections in docker-compose.yml
   - Experiment with different Gemini models

3. **Share with your team**
   - Commit docker-compose.yml (without API key!)
   - Share this guide with team members
   - Consider CI/CD integration

4. **Provide feedback**
   - Report issues on GitHub
   - Suggest improvements
   - Share your use cases

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Repomix GitHub](https://github.com/yamadashy/repomix)

---

## Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review Docker logs: `docker-compose logs`
3. Verify your configuration in docker-compose.yml
4. Open an issue on GitHub with:
   - Error message
   - Docker version
   - Operating system
   - Steps to reproduce

---

**Happy Documenting!** 🚀📄