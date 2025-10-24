# AI-Powered Documentation Generator

**Version:** 1.2.5
**Status:** Production Ready
**License:** MIT

> Transform any codebase into comprehensive technical documentation automatically using Google Gemini AI.

## Overview

An autonomous, Docker-based documentation generator that analyzes your codebase and produces professional Word (.docx) and PDF documentation with:

- **AI-Powered Content**: Intelligent section generation using Google Gemini 2.5 Flash-Lite
- **Visual Documentation**: Automated screenshots of code and live applications
- **Architecture Diagrams**: Mermaid diagram generation for system visualization
- **Multiple Formats**: Export to DOCX and PDF
- **Zero Configuration**: Fully containerized with Docker Compose

## Key Features

### Core Capabilities
- **Multi-Agent Architecture**:
  - `GeminiDocAgent`: AI content generation and planning
  - `ScreenshotAgent`: Automated code and application screenshots
  - `MermaidAgent`: Architecture diagram generation
  - `DocumentAssembler`: Professional document formatting with TOC and hyperlinks

- **Smart Rate Limiting**: Configured for Gemini 2.5 Flash-Lite free tier (15 RPM)
- **Comprehensive Documentation**: 9-15 sections based on project complexity
- **Live App Screenshots**: Capture running application interfaces
- **Cross-Platform PDF Export**: LibreOffice-based conversion

### Recent Updates (v1.2.5)
- Table of Contents with automatic numbering
- Clickable hyperlinks to external resources
- Contributors and metadata support
- Improved Mermaid diagram rendering
- Enhanced ChromeDriver compatibility

## Architecture

### Agent System

```
┌─────────────────────────────┐
│  DocumentationGenerator     │
│   (Main Orchestrator)       │
└──────────┬──────────────────┘
           │
     ┌─────┴─────┬─────────────┐
     │           │             │
     v           v             v
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Gemini   │ │Screenshot│ │ Mermaid  │
│DocAgent  │ │  Agent   │ │  Agent   │
│(Content) │ │(Selenium)│ │(Diagrams)│
└──────────┘ └────┬─────┘ └────┬─────┘
                  │             │
                  v             v
             ┌─────────┐   ┌─────────┐
             │Chromium │   │Puppeteer│
             │ Browser │   │ (mmdc)  │
             └─────────┘   └─────────┘
                  │             │
                  └──────┬──────┘
                         v
                  ┌─────────────┐
                  │  Document   │
                  │  Assembler  │
                  │ (DOCX+PDF)  │
                  └─────────────┘
```

### Browser Dependencies

**Important**: This project uses **Selenium + Chromium** (NOT Puppeteer for screenshots)

- **Selenium**: Browser automation for screenshots (via `selenium` package)
- **Chromium**: Headless browser in Docker (`chromium` + `chromium-driver` from apt)
- **Puppeteer**: ONLY used by mermaid-cli for diagram rendering
- **No Chrome**: Only Chromium is used to avoid version conflicts

The browser is **only initialized when**:
- Live URL screenshots are enabled (`LIVE_APP_ENABLED=true`)
- Code screenshots are needed for documentation sections
- Mermaid diagrams need to be rendered

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Google Gemini API key (free tier: https://aistudio.google.com/apikey)

### 1. Run with Docker Compose (Recommended)

All configuration is in `docker-compose.yml` - no separate `.env` file needed:

```bash
# 1. Clone the repository
git clone <repo-url>
cd documentation_generator

# 2. Edit docker-compose.yml and set:
#    - GEMINI_API_KEY=your_actual_api_key
#    - PROJECT_PATH=/path/to/your/project (in volumes section)
#    - PROJECT_NAME=Your Project Name

# 3. Run the generator
docker-compose up

# 4. Find output in ./output/documentation.docx
```

The container will:
- Load configuration from `docker-compose.yml`
- Mount your project as read-only at `/app/project`
- Generate documentation to `./output/`
- Save screenshots to `./screenshots/`
- Save diagrams to `./mermaid_diagrams/`
- Exit automatically when complete

### 2. Run Without Docker (Development)

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install system dependencies
# Ubuntu/Debian:
sudo apt install chromium chromium-driver libreoffice-writer
npm install -g @mermaid-js/mermaid-cli

# 4. Create .env file (copy from docker-compose.yml environment section)
cp .env.example .env
# Edit .env with your API key and settings

# 5. Run
python run_doc_generator.py
```

## Configuration

### Key Settings in docker-compose.yml

```yaml
environment:
  # API Configuration
  GEMINI_API_KEY: your_api_key_here
  GEMINI_MODEL: gemini-2.5-flash-lite  # Free tier: 15 RPM, 1000 req/day

  # Project Configuration
  PROJECT_NAME: "Your Project Name"
  PROJECT_PATH: /app/project  # Mapped from volumes
  PROJECT_DESCRIPTION: "Brief description"

  # Rate Limiting (optimized for free tier)
  GEMINI_REQUEST_DELAY: 5  # 5s = 12 req/min (under 15 RPM limit)
  GEMINI_MAX_REQUESTS_PER_MINUTE: 15

  # Screenshot Configuration
  ENABLE_SCREENSHOTS: true
  BROWSER_CHOICE: chrome  # Uses Chromium in Docker
  MAX_SCREENSHOTS_PER_DOCUMENT: 8

  # Diagram Configuration
  ENABLE_MERMAID_DIAGRAMS: true
  MAX_MERMAID_DIAGRAMS: 3

  # PDF Export
  ENABLE_PDF_EXPORT: true

  # Optional: Repomix for better context
  USE_REPOMIX: true
  REPOMIX_FILE_PATH: /app/project/repomix-output.xml
```

### Why Gemini 2.5 Flash-Lite?

This model is chosen specifically for the **free tier limits**:
- **Rate Limits**: 15 requests per minute (RPM)
- **Daily Limit**: 1,000 requests per day
- **Throughput**: 250K tokens/minute

With `GEMINI_REQUEST_DELAY=5` seconds:
- **12 requests/minute** (80% utilization)
- Safely stays under the 15 RPM limit
- Prevents rate limit errors

## Project Structure

```
documentation_generator/
├── doc_generator.py           # Main generator with all agents
├── run_doc_generator.py       # Wrapper script with validation
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container image definition
├── docker-compose.yml         # Complete configuration
├── docker-entrypoint.sh       # Container initialization
│
├── output/                    # Generated documentation
├── screenshots/               # Captured screenshots
├── mermaid_diagrams/          # Generated diagrams
│
└── Documentation:
    ├── README.md              # This file
    ├── IMPLEMENTATION_STATUS.md  # Feature status
    ├── FEATURES_v1.2.5.md     # Latest features
    ├── BUILD.md               # Build instructions
    ├── DOCKER_SETUP.md        # Docker details
    └── CHANGELOG.md           # Version history
```

## How It Works

### 4-Phase Generation Pipeline

1. **Phase 1: Load Context**
   - Reads repomix file or scans project directory
   - Gathers README, code files, structure

2. **Phase 2: Create Plan**
   - AI analyzes codebase
   - Generates 9-15 section structure
   - Identifies screenshot targets

3. **Phase 3: Generate Content**
   - AI writes each section (200-400 words)
   - Captures code screenshots
   - Generates Mermaid diagrams
   - Captures live app screenshots

4. **Phase 4: Assemble Document**
   - Creates Word document with TOC
   - Embeds images and diagrams
   - Adds hyperlinks and formatting
   - Exports to PDF (optional)

### Optimization Features

**Section Limits**: Adjusts 9-15 sections based on project size
**Screenshot Priority**: Focuses on installation, config, architecture, usage
**Diagram Limits**: Maximum 3 diagrams per document
**Smart Caching**: Reuses context across requests

## Agent Details

### GeminiDocAgent
**Location**: `doc_generator.py:119-709`

- **Purpose**: AI interaction layer
- **Methods**:
  - `create_documentation_plan()`: Analyzes code and creates structure
  - `generate_section_content()`: Writes section text
  - `identify_screenshot_targets()`: Suggests files to screenshot
  - `_make_request()`: Rate-limited API calls with retry logic

**Rate Limiting**:
- Per-minute request tracking
- Type-specific delays (plan, section, screenshot, diagram)
- Exponential backoff on errors

### ScreenshotAgent
**Location**: `doc_generator.py:711-934`

- **Purpose**: Visual documentation
- **Browser**: Selenium with Chromium (headless)
- **Capabilities**:
  - Code file screenshots with syntax highlighting
  - Directory tree visualization
  - Live application screenshots
- **Configuration**:
  - `ENABLE_SCREENSHOTS`: Enable/disable
  - `BROWSER_CHOICE`: chrome (uses Chromium in Docker)
  - `SCREENSHOT_WAIT_TIME`: Page load delay

### MermaidAgent
**Location**: `doc_generator.py:936-1179`

- **Purpose**: Architecture diagram generation
- **Rendering Strategies**:
  1. mermaid-cli (mmdc) with Puppeteer
  2. mermaid.ink online API
  3. Fallback: Save code as text
- **Diagram Types**: Flowcharts, sequence, class, state, ER diagrams
- **Browser**: Puppeteer (used by mmdc, NOT by Python directly)

### DocumentAssembler
**Location**: `doc_generator.py:1181-1824`

- **Purpose**: Word document creation
- **Features**:
  - Professional title page with metadata
  - Table of Contents with numbering
  - Clickable hyperlinks
  - Contributors list
  - Formatted code blocks
  - Image embedding
  - PDF export (LibreOffice)

## Docker Details

### Image Specification

- **Base**: `python:3.13-slim`
- **Size**: ~800MB (includes Chromium, Node.js, LibreOffice)
- **User**: Non-root user `docgen` (UID 1000)
- **Entrypoint**: Permission fixes + app execution

### Installed Components

**Python Packages** (from `requirements.txt`):
- `google-generativeai`: Gemini API client
- `selenium`: Browser automation
- `python-docx`: Word document generation
- `Pillow`: Image processing
- `python-dotenv`: Environment management
- `webdriver-manager`: Driver management (bypassed in Docker)

**System Packages**:
- `chromium`: Headless browser
- `chromium-driver`: ChromeDriver (matched version)
- `nodejs` + `npm`: For mermaid-cli
- `libreoffice-writer`: PDF export
- `fonts-liberation`: Better rendering

**Node.js Packages**:
- `@mermaid-js/mermaid-cli`: Diagram rendering

### Volume Mounts

```yaml
volumes:
  - ./output:/app/output              # Documentation output
  - ./screenshots:/app/screenshots    # Screenshot storage
  - ./mermaid_diagrams:/app/mermaid_diagrams  # Diagram storage
  - /path/to/project:/app/project     # Your codebase (read-only)
```

### Network Mode

```yaml
network_mode: host  # For Linux - enables localhost screenshot capture
```

On Mac/Windows, use `host.docker.internal` instead of `127.0.0.1` for live URLs.

## Repomix Integration

For best results, generate a repomix file before running:

```bash
# Install repomix (if not already installed)
npm install -g repomix

# Generate context file
repomix /path/to/your/project -o repomix-output.xml

# Place in project root or specify path in docker-compose.yml
```

**Benefits**:
- Better AI understanding of codebase
- Faster context loading
- Respects .gitignore automatically

Set in `docker-compose.yml`:
```yaml
USE_REPOMIX: true
REPOMIX_FILE_PATH: /app/project/repomix-output.xml
```

## Troubleshooting

### Common Issues

**1. Container exits immediately**
- Check `docker-compose logs` for errors
- Verify `GEMINI_API_KEY` is set correctly
- Ensure `PROJECT_PATH` volume mount is correct

**2. API rate limit errors**
- Increase `GEMINI_REQUEST_DELAY` (try 7 or 10 seconds)
- Reduce `MAX_SECTIONS` to generate less content
- Check daily quota (1000 requests/day for free tier)

**3. Screenshot failures**
- Chromium version mismatch (should not happen with Docker)
- Increase `SCREENSHOT_WAIT_TIME` for slow-loading pages
- Check live app URLs are accessible from container

**4. Mermaid diagrams not rendering**
- Check mmdc is installed: `docker-compose exec doc-generator mmdc --version`
- Diagram too complex (reduce nodes to 5-7)
- Use mermaid.ink fallback (automatic)

**5. PDF export fails**
- LibreOffice not installed (should be in Docker)
- Large document timeout (increase conversion timeout)
- Disable PDF: `ENABLE_PDF_EXPORT=false`

### Debug Mode

Enable verbose logging:
```yaml
environment:
  PYTHONUNBUFFERED: 1  # Real-time output
```

View logs:
```bash
docker-compose up        # Attached mode (see live output)
docker-compose logs -f   # Follow logs
```

## Version History

**v1.2.5** (Current)
- Table of Contents with automatic numbering
- Clickable hyperlinks to external resources
- Contributors and organization metadata
- Improved Mermaid diagram sizing
- Enhanced ChromeDriver compatibility

**v1.2.4**
- Fixed screenshot failures in Docker
- Improved Mermaid diagram rendering
- Better ChromeDriver version matching

**v1.2.3**
- Rate limiting optimizations
- Section count optimization
- Exponential backoff on errors

See [CHANGELOG.md](CHANGELOG.md) for complete history.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Development workflow
- Branch strategy
- Testing procedures

## License

MIT License - see LICENSE file

## Credits

- **AI Model**: Google Gemini 2.5 Flash-Lite
- **Screenshot Engine**: Selenium + Chromium
- **Diagram Rendering**: Mermaid.js + mermaid-cli
- **Document Generation**: python-docx + LibreOffice
- **Containerization**: Docker + Docker Compose

## Support

- **Issues**: https://github.com/your-repo/issues
- **Documentation**: See `*.md` files in root directory
- **API Reference**: https://ai.google.dev/gemini-api/docs

## Roadmap

- [ ] Web interface for configuration
- [ ] Support for additional output formats (Markdown, HTML)
- [ ] Multi-language documentation support
- [ ] Incremental documentation updates
- [ ] CI/CD integration examples
- [ ] Custom template support

---

**Generated with AI**
Documentation Generator v1.2.5

