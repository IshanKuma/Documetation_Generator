# Changelog

All notable changes to the Documentation Generator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.5] - 2025-10-24

### Added
- **Table of Contents**: Auto-numbered TOC with hierarchical section listing
- **Hyperlink Support**: Automatic URL detection and clickable links in generated docs
- **Contributors Metadata**: Support for author, contributors list, and organization info
  - Environment variables: `DOCUMENTATION_AUTHOR`, `DOCUMENTATION_CONTRIBUTORS`, `DOCUMENTATION_ORGANIZATION`

### Changed
- **Complete Documentation Rewrite**:
  - **README.md**: Comprehensive rewrite (~500 lines) with accurate architecture, browser dependencies clarification, Docker setup guide, and troubleshooting
  - **IMPLEMENTATION_STATUS.md**: Complete rewrite (~700 lines) with feature matrix, testing results, performance metrics, and version roadmap
- **Browser Dependencies Clarified**:
  - Documented that Selenium + Chromium is used for screenshots (Python direct)
  - Documented that Puppeteer is ONLY used by mermaid-cli for diagrams (Node.js)
  - No Chrome dependency (only Chromium)
- **Model Information Corrected**: Documentation now correctly shows `gemini-2.5-flash-lite` (not Pro)
- **Configuration Guide**: Docker-compose.yml fully documented as single source of configuration

### Improved
- Mermaid diagram generation prompts (5-7 nodes max, <500 chars)
- Diagram size limits to prevent rendering failures
- Error handling for diagram rendering with better fallback messages

---

## [1.2.4] - 2025-10-15

### Fixed
- ChromeDriver version mismatch in Docker
- Screenshot failures in containerized environment
- Mermaid diagram rendering issues

### Changed
- Use system ChromeDriver from apt (matches system Chromium version)
- Set `CHROMEDRIVER_PATH=/usr/bin/chromedriver` in Docker
- Improved Puppeteer configuration for mermaid-cli

---

## [1.2.2] - 2025-10-15

### Added
- **Intelligent Rate Limiting**: Configurable request delays to prevent hitting Gemini API limits
  - Default delay increased from 2s to 5s (12 req/min, safely under 15 req/min limit)
  - Per-request-type delays (plan, section, screenshot, diagram)
  - Request counter with per-minute tracking
  - Exponential backoff on 429 errors
  - Environment variables: `GEMINI_REQUEST_DELAY`, `GEMINI_PLAN_REQUEST_DELAY`, `GEMINI_SECTION_REQUEST_DELAY`, `GEMINI_SCREENSHOT_REQUEST_DELAY`, `GEMINI_DIAGRAM_REQUEST_DELAY`, `GEMINI_MAX_REQUESTS_PER_MINUTE`, `GEMINI_MAX_RETRIES`, `GEMINI_BASE_BACKOFF_DELAY`

- **Content Generation Optimization**: Flexible controls to reduce API calls
  - Section count optimization (9-15 sections based on project size)
  - Selective screenshot generation (max 8 per document)
  - Priority-based screenshot selection
  - Mermaid diagram limits (max 3 per document)
  - Environment variables: `MIN_SECTIONS`, `MAX_SECTIONS`, `MAX_SCREENSHOTS_PER_DOCUMENT`, `SCREENSHOT_PRIORITY_SECTIONS`, `MAX_MERMAID_DIAGRAMS`

- **Docker Improvements**:
  - ChromeDriver automatic version matching via `webdriver-manager`
  - System ChromeDriver support via `CHROMEDRIVER_PATH` env var
  - Proper container lifecycle management (no restart loops)
  - Updated `.dockerignore` with archives and unused files

- **Configuration Enhancements**:
  - Comprehensive environment variable coverage in `docker-compose.yml`
  - No separate `.env` file needed for deployment
  - Better documentation of all config options

### Changed
- Default `GEMINI_REQUEST_DELAY` increased from 2s to 5s for better stability
- Chrome/ChromeDriver installation strategy (automatic matching instead of fixed versions)
- Container restart policy set to `"no"` to prevent infinite loops

### Fixed
- Docker container restart loop issues
- Chrome/ChromeDriver version mismatch errors
- API rate limit violations during large documentation generation

### Removed
- `test_json_fix.py` (obsolete test file)

## [1.0] - Initial Release

### Added
- AI-powered documentation generation using Google Gemini 2.5 Pro
- Screenshot capture capabilities (code examples)
- Mermaid diagram generation
- DOCX and PDF output formats
- Docker containerization
- Comprehensive configuration via environment variables
