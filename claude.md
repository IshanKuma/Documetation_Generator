# Documentation Generator - Project Context

> **Project:** AI-Powered Documentation Generator (Gemini Edition)
> **Last Updated:** 2025-10-09
> **Version:** 2.0.0
> **Stack:** Python 3.8+, Google Gemini API, Selenium, python-docx

---

## 🎯 Project Overview

An **automated technical documentation generation system** that creates comprehensive Word (.docx) and PDF documentation from codebases using Google's Gemini 2.5 Pro AI model. This tool analyzes code, captures screenshots, and generates professional documentation with minimal human intervention.

**Core Purpose:** Transform any software project into professionally formatted technical documentation by:
1. Analyzing codebase structure (via repomix or directory scan)
2. Generating contextual documentation sections using AI
3. Capturing automated screenshots of code, directory structure, and live applications
4. Assembling everything into polished Word/PDF documents

---

## 🌍 Global Guidelines

This project follows the global Claude guidelines located at:
- **Path:** `/home/user/Downloads/global_claude_md.md`
- **Reference:** All coding standards, git protocols, and best practices from the global file apply

### Key Principles (from Global Guidelines)
- ✅ **Safety first**: Always commit before major refactoring
- ✅ **Incremental progress**: Small, tested steps with frequent commits
- ✅ **Type hints required**: All Python functions must have type annotations
- ✅ **Error handling**: Proper exception handling with informative messages
- ✅ **Code documentation**: Detailed comments explaining logic and decisions

### Project-Specific Requirements

#### Command Explanations (Critical)
**ALL commands, code changes, and operations MUST be explained BEFORE execution.**

This requirement applies to:
- ✅ **Bash commands**: Explain what the command does and why before running
  ```bash
  # Example:
  # Explanation: "Update .env file to set PROJECT_PATH to current directory"
  sed -i 's|PROJECT_PATH=.*|PROJECT_PATH=/home/user/Desktop/documentation_generator|' .env
  ```

- ✅ **File operations**: Explain what file is being created/modified and why
  ```python
  # Example:
  # Explanation: "Creating requirements.txt with all Python dependencies for the documentation generator"
  with open('requirements.txt', 'w') as f:
      f.write(...)
  ```

- ✅ **Code changes**: Explain the logic change and its impact
  ```python
  # Example:
  # Explanation: "Changing default Gemini model from gemini-2.0-flash-exp to gemini-2.5-pro
  #              because gemini-2.5-pro provides better documentation quality"
  self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-pro')
  ```

- ✅ **Agent tasks**: When launching agents, explain what task they're performing
  ```
  # Example:
  "Launching agent to add PDF export functionality. This will:
   1. Add save_as_pdf() method to DocumentAssembler
   2. Support Windows (python-docx2pdf), Linux/macOS (LibreOffice)
   3. Include comprehensive error handling and installation guidance"
  ```

**Why this requirement:**
- User needs to understand what's happening in real-time
- Builds trust and transparency in AI operations
- Helps user learn the system architecture
- Makes debugging easier if something goes wrong
- Provides educational value beyond just completing the task

**Format:**
```
[Brief explanation of what will be done and why]
[Command/code execution]
[Result/verification]
```

**Non-compliance:**
❌ Running commands without explanation
❌ Providing only summary at the end
❌ Assuming user knows what the command does

---

## 🏗️ Project Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Documentation Generator                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. GeminiDocAgent                                          │
│     ├── API Communication with Gemini 2.5 Pro              │
│     ├── Documentation Plan Creation                         │
│     ├── Content Generation (per section)                    │
│     └── Screenshot Target Identification                    │
│                                                              │
│  2. ScreenshotAgent                                         │
│     ├── Selenium WebDriver (Chrome/Firefox)                │
│     ├── Code File Rendering with Syntax Highlighting       │
│     ├── Directory Tree Visualization                        │
│     └── Live Application Screenshot Capture                 │
│                                                              │
│  3. DocumentAssembler                                       │
│     ├── Word Document Generation (python-docx)             │
│     ├── PDF Export (future enhancement)                    │
│     ├── Section Formatting & Styling                        │
│     └── Image & Code Block Embedding                        │
│                                                              │
│  4. DocumentationGenerator (Orchestrator)                   │
│     └── Coordinates all agents through 4-phase pipeline    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Input → Context Loading → AI Planning → Content Generation → Assembly → Output
  ↓          ↓                ↓              ↓                  ↓         ↓
.env    repomix.txt      Gemini API    Section Text      python-docx  .docx
                         (Plan)         + Screenshots                  .pdf
```

---

## 📂 Project Structure

```
documentation_generator/
├── doc_generator.py           # Main application (all agents & logic)
├── run_doc_generator.py       # Wrapper script with validation
├── claude.md                  # This file - project context
├── .env                       # Configuration (API keys, paths)
├── .env.example              # Template for new users
├── requirements.txt          # Python dependencies
├── setup.sh                  # One-command setup script (future)
├── project_readme.md         # User-facing documentation
├── setup_guide_gemini.md     # Complete setup instructions
├── system_diagram.mermaid    # Visual system architecture
├── output/                   # Generated documentation
│   └── documentation.docx
├── screenshots/              # Captured images
│   ├── src_main.py.png
│   └── directory_structure.png
└── repomix-output.txt       # Optional: consolidated codebase

Future additions:
├── tests/                    # Unit & integration tests
│   ├── test_gemini_agent.py
│   ├── test_screenshot_agent.py
│   └── test_assembler.py
├── templates/                # Custom doc templates
└── examples/                 # Sample outputs
```

---

## 🔧 Development Environment

### Local Setup
- **Location:** `/home/user/Desktop/documentation_generator`
- **Sync:** Directory synced via Synology Drive to NAS server
- **Shell:** Zsh with Oh My Zsh (Powerlevel10k theme)
- **Python Version:** 3.8+ (tested on 3.10)

### Known Issues & Fixes

#### Seqrite Antivirus Interference
**Problem:** Seqrite's file operation wrappers (`/usr/lib/Seqrite/ClientAgent/cmd/`) cause silent failures with file operations.

**Solution:** Aliases added to `~/.zshrc` (lines 61-65) bypass Seqrite wrappers:
```bash
alias touch='/bin/touch'
alias mkdir='/bin/mkdir'
alias rm='/bin/rm'
alias mv='/bin/mv'
alias cp='/bin/cp'
```

**Impact on This Project:**
- File creation operations (saving .docx, screenshots) may fail without these aliases
- Always verify output directories exist before running generator
- Use absolute paths in `.env` to avoid path resolution issues

---

## ⚙️ Configuration (.env)

### Environment Variables Explained

#### 🔑 API Configuration
```bash
# Required: Get free key from https://aistudio.google.com/apikey
GEMINI_API_KEY=AIzaSy...
# Purpose: Authenticates API requests to Google Gemini
# Security: Never commit actual keys to version control

# Model Selection
GEMINI_MODEL=gemini-2.5-pro
# Options: gemini-2.5-pro, gemini-2.0-flash-exp
# Explanation: gemini-2.5-pro offers better quality, flash is faster/cheaper
# Default: gemini-2.5-pro (as of 2025-10-09)

# Generation Settings
GEMINI_TEMPERATURE=0.7
# Range: 0.0 (deterministic) to 1.0 (creative)
# Purpose: Controls randomness in AI responses
# Recommendation: 0.7 for balanced technical writing

GEMINI_MAX_OUTPUT_TOKENS=8000
# Explanation: Maximum tokens per API response
# Impact: Longer sections need higher limits

GEMINI_REQUEST_DELAY=2
# Purpose: Seconds between API calls to respect rate limits
# Free tier: 15 requests/minute → 4 seconds between requests is safe
# Paid tier: Can reduce to 1-2 seconds
```

#### 📁 Project Configuration
```bash
PROJECT_NAME=My Awesome Project
# Purpose: Appears on title page and headers
# Tip: Use descriptive names for multiple projects

PROJECT_PATH=/absolute/path/to/your/project
# IMPORTANT: Must be absolute path, not relative (~/project won't work)
# Purpose: Root directory of the project to document
# Special: Set to "/" to document documentation_generator itself

PROJECT_DESCRIPTION=Brief project description
# Purpose: Appears on title page under project name
# Optional but recommended for context
```

#### 🗂️ Repomix Configuration
```bash
USE_REPOMIX=true
# Purpose: Use consolidated codebase file instead of directory scan
# Benefits: Better context, more accurate docs, fewer API calls
# Setup: repomix /path/to/project -o repomix-output.txt

REPOMIX_FILE_PATH=./repomix-output.txt
# Purpose: Path to repomix output file (relative to this directory)
# Note: Copy repomix file to documentation_generator folder
```

#### 📤 Output Configuration
```bash
OUTPUT_DIRECTORY=./output
# Purpose: Where generated .docx/.pdf files are saved
# Note: Created automatically if doesn't exist

OUTPUT_FILENAME=documentation.docx
# Purpose: Name of generated document
# Tip: Include project name for multiple projects

SCREENSHOTS_DIRECTORY=./screenshots
# Purpose: Where captured screenshots are stored
# Note: Created automatically, can get large
```

#### 📸 Screenshot Configuration
```bash
ENABLE_SCREENSHOTS=true
# Purpose: Enable/disable screenshot capture
# Performance: Disabling speeds up generation significantly

BROWSER_CHOICE=chrome
# Options: chrome, firefox
# Purpose: Which browser Selenium uses for screenshots
# Requirement: Browser must be installed

SCREENSHOT_WAIT_TIME=3
# Purpose: Seconds to wait for page load before screenshot
# Troubleshooting: Increase if screenshots are blank (try 5-7)

MAX_CODE_BLOCK_LINES=50
# Purpose: Maximum lines of code to screenshot
# Reason: Prevents huge screenshots, keeps docs readable
```

#### 🌐 Live Application Screenshots
```bash
LIVE_APP_ENABLED=false
# Purpose: Capture screenshots of running application
# Usage: Start app first, then run generator

# Add unlimited URLs with pattern LIVE_APP_URL_<NAME>
LIVE_APP_URL_HOME=http://localhost:3000
LIVE_APP_URL_DASHBOARD=http://localhost:3000/dashboard
LIVE_APP_URL_API_DOCS=http://localhost:8000/docs
# Pattern: LIVE_APP_URL_* where * is descriptive name
# Tip: Capture key pages that showcase your app
```

#### 📊 Section Control
```bash
INCLUDE_OVERVIEW=true
INCLUDE_ARCHITECTURE=true
INCLUDE_INSTALLATION=true
INCLUDE_USAGE=true
INCLUDE_API_REFERENCE=true
INCLUDE_DEVELOPMENT_GUIDE=true
INCLUDE_TROUBLESHOOTING=true
INCLUDE_DEPLOYMENT=false
# Purpose: Toggle which sections appear in final document
# Use case: Skip irrelevant sections (e.g., no API for CLI tools)
```

#### 🔬 Advanced Settings
```bash
MAX_FILE_SIZE_KB=100
# Purpose: Skip files larger than this when scanning directory
# Reason: Avoid loading huge binary files or data files

EXCLUDED_DIRECTORIES=node_modules,.git,__pycache__,venv,.venv,dist,build
# Purpose: Directories to ignore during scan
# Impact: Reduces noise, speeds up processing
# Customize: Add your cache/build directories
```

---

## 🚀 Usage Workflows

### Workflow 1: Basic Usage (No Repomix)
```bash
# 1. Configure .env
nano .env
# Set: GEMINI_API_KEY, PROJECT_NAME, PROJECT_PATH
# Set: USE_REPOMIX=false

# 2. Run generator
python run_doc_generator.py

# 3. Find output
ls output/
# → documentation.docx
```

**When to use:** Quick documentation for small projects (<50 files)

---

### Workflow 2: High-Quality Documentation (With Repomix)
```bash
# 1. Generate repomix file for target project
cd /path/to/target/project
repomix . -o repomix-output.txt

# 2. Copy to documentation_generator folder
cp repomix-output.txt /home/user/Desktop/documentation_generator/

# 3. Update .env
nano /home/user/Desktop/documentation_generator/.env
# Set: USE_REPOMIX=true
# Set: REPOMIX_FILE_PATH=./repomix-output.txt

# 4. Run generator
cd /home/user/Desktop/documentation_generator
python run_doc_generator.py

# 5. Review output
libreoffice output/documentation.docx
```

**When to use:** Best quality documentation, large projects, complex codebases

**Benefits:**
- Better context for AI (entire codebase in one file)
- More accurate technical details
- Fewer API calls (faster + cheaper)
- Consistent understanding across sections

---

### Workflow 3: With Live Application Screenshots
```bash
# 1. Start your application
cd /path/to/your/project
npm start  # or: python manage.py runserver, etc.
# Wait for app to fully load (e.g., http://localhost:3000)

# 2. Open new terminal
cd /home/user/Desktop/documentation_generator

# 3. Update .env
nano .env
# Set: LIVE_APP_ENABLED=true
# Add: LIVE_APP_URL_HOME=http://localhost:3000
# Add: LIVE_APP_URL_DASHBOARD=http://localhost:3000/dashboard
# (Add more as needed)

# 4. Run generator
python run_doc_generator.py
# When prompted "Is your app running? (y/n)": type 'y'

# 5. Generator captures screenshots while app runs
# 6. Keep app running until "Phase 3.5 complete" appears
```

**When to use:** Web applications, APIs with documentation pages, dashboards

**Tips:**
- Ensure app is fully loaded (check browser manually first)
- Use descriptive URL names (LIVE_APP_URL_ADMIN, not LIVE_APP_URL_1)
- Capture 3-5 key pages (home, main features, admin panel)

---

### Workflow 4: Multiple Projects
```bash
# Strategy: Use separate .env files

# Project 1
cp .env .env.project1
nano .env.project1  # Configure for project 1
python run_doc_generator.py  # Uses .env by default

# Project 2
cp .env .env.project2
nano .env.project2  # Configure for project 2
cp .env.project2 .env
python run_doc_generator.py

# Or: Create wrapper script
./generate_docs.sh project1  # Loads .env.project1
./generate_docs.sh project2  # Loads .env.project2
```

---

## 🔄 Development Workflow

### Making Changes to doc_generator.py

#### Before Changes
```bash
# 1. Ensure working tree is clean
git status

# 2. Create feature branch (if major change)
git checkout -b feature/add-markdown-export

# 3. Run generator once to verify current state
python run_doc_generator.py
# This creates baseline output to compare against
```

#### During Development
```bash
# 1. Edit code with detailed comments
# Remember: Every non-trivial function needs explanation

# 2. Test incrementally
python doc_generator.py  # Direct execution for testing
# Or create minimal test script

# 3. Commit frequently (every 50-100 lines of working code)
git add doc_generator.py
git commit -m "feat(generator): add markdown export functionality

- Implemented MarkdownExporter class
- Added .md output format support
- Updated DocumentationGenerator to support multiple formats"
```

#### After Changes
```bash
# 1. Full integration test
python run_doc_generator.py

# 2. Verify output quality
diff output/documentation.docx output/documentation.backup.docx

# 3. Update documentation
nano project_readme.md  # Add new feature to README
nano claude.md          # Update this file if architecture changed

# 4. Final commit
git add .
git commit -m "docs: update documentation for markdown export"
```

---

## 🧪 Testing Strategy

### Current State
- ⚠️ **No automated tests yet** (manual testing only)
- Future enhancement: Unit tests for each agent

### Manual Testing Checklist

#### Pre-Release Testing
```bash
# Test 1: Basic generation (no repomix, no screenshots)
# .env: USE_REPOMIX=false, ENABLE_SCREENSHOTS=false
python run_doc_generator.py
# Expected: Fast completion, basic docs

# Test 2: Full generation (with repomix, with screenshots)
# .env: USE_REPOMIX=true, ENABLE_SCREENSHOTS=true
python run_doc_generator.py
# Expected: High-quality docs with images

# Test 3: Live app capture
# .env: LIVE_APP_ENABLED=true
# Start test app first, then:
python run_doc_generator.py
# Expected: App screenshots embedded

# Test 4: Error handling
# .env: GEMINI_API_KEY=invalid
python run_doc_generator.py
# Expected: Clear error message, graceful exit

# Test 5: Missing dependencies
pip uninstall selenium
python run_doc_generator.py
# Expected: Import error with helpful message
pip install selenium  # Fix
```

#### Output Validation
```bash
# 1. Check file exists
ls -lh output/documentation.docx
# Should be 500KB - 5MB depending on screenshots

# 2. Open in Word/LibreOffice
libreoffice output/documentation.docx
# Verify:
# - Title page formatted correctly
# - All sections present
# - Screenshots visible (not broken)
# - Code blocks formatted properly
# - No placeholder text like "[IMAGE: ...]"

# 3. Check screenshots
ls screenshots/
# Should contain:
# - directory_structure.png
# - src_*.png (code files)
# - live_*.png (if live app enabled)
```

### Future: Automated Testing
```python
# tests/test_gemini_agent.py (planned)
def test_create_documentation_plan():
    """Test that Gemini generates valid JSON plan."""
    agent = GeminiDocAgent()
    context = "Sample project..."
    plan = agent.create_documentation_plan(context, "Test Project")
    assert len(plan.sections) > 0
    assert plan.title == "Test Project Documentation"

# tests/test_screenshot_agent.py (planned)
def test_capture_code_file():
    """Test screenshot generation for code files."""
    agent = ScreenshotAgent()
    path = agent.capture_code_file("doc_generator.py")
    assert os.path.exists(path)
    assert os.path.getsize(path) > 1000  # Not empty

# Run tests
pytest tests/ --cov=. --cov-report=html
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "GEMINI_API_KEY not found"
```bash
# Cause: .env file missing or key not set
# Fix:
ls -la .env  # Verify file exists
cat .env | grep GEMINI_API_KEY  # Check key present
nano .env  # Add: GEMINI_API_KEY=AIzaSy...
```

#### 2. "Project path does not exist"
```bash
# Cause: Relative path used instead of absolute
# Wrong: PROJECT_PATH=~/projects/myapp
# Wrong: PROJECT_PATH=../myapp
# Correct: PROJECT_PATH=/home/user/projects/myapp

# Fix:
realpath /path/to/project  # Get absolute path
nano .env  # Update PROJECT_PATH with absolute path
```

#### 3. Screenshots are blank/white
```bash
# Cause: Page not loaded before screenshot
# Fix:
nano .env
# Change: SCREENSHOT_WAIT_TIME=3
# To:     SCREENSHOT_WAIT_TIME=7

# Or try different browser:
# Change: BROWSER_CHOICE=chrome
# To:     BROWSER_CHOICE=firefox
```

#### 4. "Rate limit exceeded" (Gemini API)
```bash
# Cause: Too many requests too fast
# Free tier: 15 requests/minute

# Fix:
nano .env
# Change: GEMINI_REQUEST_DELAY=2
# To:     GEMINI_REQUEST_DELAY=5

# Or wait 60 seconds and retry
```

#### 5. ChromeDriver version mismatch
```bash
# Symptom: "SessionNotCreatedException: Chrome version mismatch"
# Cause: webdriver-manager couldn't auto-download driver

# Fix:
pip uninstall webdriver-manager
pip install webdriver-manager --upgrade
# Or manually:
google-chrome --version  # Check version
# Download matching driver from: https://chromedriver.chromium.org/
```

#### 6. "ModuleNotFoundError: No module named 'google.generativeai'"
```bash
# Cause: Dependencies not installed
# Fix:
pip install -r requirements.txt
# Or:
pip install google-generativeai python-dotenv python-docx selenium webdriver-manager
```

#### 7. Selenium can't find browser
```bash
# Symptom: "WebDriverException: chrome not found"
# Fix:
which google-chrome  # Verify Chrome installed
# Or try Firefox:
nano .env
# Set: BROWSER_CHOICE=firefox
```

---

## 📊 Performance Optimization

### Speed vs Quality Tradeoffs

#### Fast Mode (2-3 minutes)
```bash
# .env settings:
USE_REPOMIX=false
ENABLE_SCREENSHOTS=false
GEMINI_REQUEST_DELAY=1
MAX_FILE_SIZE_KB=50
```
**Use case:** Quick drafts, iterating on structure

#### Balanced Mode (5-8 minutes)
```bash
# .env settings:
USE_REPOMIX=true
ENABLE_SCREENSHOTS=true
GEMINI_REQUEST_DELAY=2
MAX_FILE_SIZE_KB=100
```
**Use case:** Production documentation, most projects

#### High-Quality Mode (10-15 minutes)
```bash
# .env settings:
USE_REPOMIX=true
ENABLE_SCREENSHOTS=true
LIVE_APP_ENABLED=true
GEMINI_REQUEST_DELAY=3
MAX_FILE_SIZE_KB=200
SCREENSHOT_WAIT_TIME=5
```
**Use case:** Final deliverables, client presentations

### Resource Usage
- **API Calls:** ~10-25 per run (stays within free tier)
- **Disk Space:** Screenshots can use 5-50 MB
- **Memory:** ~200-500 MB during generation
- **Network:** ~2-5 MB API traffic per run

---

## 🔐 Security Best Practices

### API Key Management
```bash
# ✅ Good: Use environment variables
GEMINI_API_KEY=AIzaSy... (in .env)

# ❌ Bad: Hardcode in Python
api_key = "AIzaSy..."  # Never do this!

# ✅ Good: Add to .gitignore
echo ".env" >> .gitignore
echo "*.backup.env" >> .gitignore

# ✅ Good: Use .env.example for sharing
cp .env .env.example
nano .env.example  # Remove actual key
# Share .env.example, not .env
```

### Sensitive Data in Screenshots
```bash
# Risk: Screenshots might capture sensitive data from code

# Mitigation 1: Review screenshots before sharing
ls screenshots/
# Check each .png for secrets, API keys, tokens

# Mitigation 2: Exclude sensitive files
nano .env
# Add to: EXCLUDED_DIRECTORIES
# Example: EXCLUDED_DIRECTORIES=node_modules,.git,secrets,config/prod

# Mitigation 3: Manual review of output
libreoffice output/documentation.docx
# Search for: password, api_key, secret, token
```

### Repomix File Security
```bash
# Risk: repomix-output.txt contains entire codebase

# ✅ Add to .gitignore
echo "repomix-output.txt" >> .gitignore

# ✅ Delete after generation
python run_doc_generator.py
rm repomix-output.txt  # Clean up

# ✅ Store securely if keeping
chmod 600 repomix-output.txt  # Only owner can read
```

---

## 🔄 Git Workflow

### Commit Guidelines (from Global Standards)

#### Before Committing
```bash
# 1. Check status
git status

# 2. Review changes
git diff

# 3. Stage files
git add doc_generator.py
# Or: git add -p  # Interactive staging
```

#### Commit Format
```bash
# Pattern: <type>(<scope>): <subject>

# Examples:
git commit -m "feat(generator): add PDF export functionality"
git commit -m "fix(screenshot): resolve blank image issue on slow systems"
git commit -m "refactor(gemini): improve error handling for API failures"
git commit -m "docs(readme): add installation instructions for Windows"
git commit -m "chore(deps): update selenium to 4.18.0"
```

#### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring (no behavior change)
- `docs`: Documentation only
- `style`: Code formatting (no logic change)
- `test`: Adding/updating tests
- `chore`: Maintenance (deps, config, etc.)

#### When to Commit
✅ **Commit after:**
- Successfully implementing a feature
- Fixing a bug and verifying it works
- Completing a refactoring that passes tests
- Before risky changes (safety checkpoint)
- Every 50-100 lines of working code

⚠️ **Ask before committing:**
- Major architectural changes
- Updating dependencies
- Changes affecting multiple files
- Anything that might break existing functionality

---

## 🎯 Future Enhancements

### Planned Features

#### Priority 1 (High Impact)
- [ ] **PDF Export:** Add `DocumentAssembler.save_as_pdf()` method
  - Use `python-docx2pdf` or `reportlab`
  - Maintain formatting from Word version

- [ ] **Markdown Export:** Add `MarkdownExporter` class
  - For GitHub/GitLab wikis
  - Preserve code blocks and images

- [ ] **Custom Templates:** Support user-defined document styles
  - `templates/corporate.docx` for company branding
  - `templates/minimal.docx` for simple docs

#### Priority 2 (Quality of Life)
- [ ] **Progress Bar:** Visual feedback during generation
  - Use `tqdm` library
  - Show: "Phase 2/4: Generating section 3/9..."

- [ ] **Resume on Failure:** Save progress and resume
  - Checkpoint after each section
  - Skip completed sections on retry

- [ ] **Dry Run Mode:** Preview what will be generated
  - Show plan without calling Gemini
  - Estimate API costs

#### Priority 3 (Advanced)
- [ ] **Multi-Language Support:** Detect code language
  - Python, JavaScript, Java, Go, Rust, etc.
  - Customize documentation structure per language

- [ ] **Integration Testing:** Screenshot test results
  - Capture pytest/jest output
  - Include test coverage reports

- [ ] **Version Comparison:** Diff documentation
  - Compare v1.0 vs v2.0 docs
  - Highlight changed sections

### Enhancement Ideas (Community Suggestions)
- [ ] **CLI Arguments:** Override .env with `--project-path=/path`
- [ ] **Batch Processing:** Document multiple projects in one run
- [ ] **Docker Support:** Containerize entire system
- [ ] **Web UI:** Simple Flask/FastAPI frontend
- [ ] **Plugin System:** Custom screenshot types, exporters

---

## 📚 Code Documentation Standards

### Required Comments

#### Every Class
```python
class GeminiDocAgent:
    """Handles all Google Gemini API interactions for documentation generation.

    This agent is responsible for:
    1. Creating documentation structure (sections, hierarchy)
    2. Generating detailed content for each section
    3. Identifying which code files/areas need screenshots

    Attributes:
        model_name (str): Gemini model identifier (e.g., 'gemini-2.5-pro')
        temperature (float): AI creativity setting (0.0-1.0)
        max_tokens (int): Maximum response length
        request_delay (int): Seconds to wait between API calls (rate limiting)
        model (GenerativeModel): Initialized Gemini model instance

    Rate Limits (Free Tier):
        - 15 requests per minute
        - 1,500 requests per day
        - 1M tokens/minute input
        - 32K tokens/minute output

    Example:
        agent = GeminiDocAgent()
        plan = agent.create_documentation_plan(context, "My Project")
        content = agent.generate_section_content(plan.sections[0], context)
    """
```

#### Every Non-Trivial Function
```python
def _extract_code_blocks(self, content: str) -> List[str]:
    """Extract code blocks from markdown-formatted content.

    Searches for code blocks delimited by:
    - CODE_BLOCK_START / CODE_BLOCK_END markers (custom format)
    - Triple backticks ``` (standard markdown)

    Handles nested structures and language identifiers (```python, ```javascript).

    Args:
        content (str): Raw text content from Gemini API response, may contain
                      mixed text and code blocks

    Returns:
        List[str]: Extracted code blocks with markers/backticks removed.
                   Empty list if no code blocks found.

    Example:
        content = "Here's code:\n```python\nprint('hello')\n```\nMore text"
        blocks = agent._extract_code_blocks(content)
        # Returns: ["print('hello')"]

    Note:
        - Language identifiers (```python) are stripped
        - Indentation is preserved within blocks
        - Handles incomplete blocks gracefully (no crash)
    """
```

#### Complex Logic Blocks
```python
# Context: We're parsing Gemini's JSON response, but it sometimes includes
# markdown code block wrappers (```json ... ```) despite prompt instructions.
# This cleanup ensures we can parse the JSON regardless of format.
response = response.strip()
if response.startswith('```'):
    # Remove markdown code block markers
    # Example input: "```json\n{\"title\": \"Docs\"}\n```"
    # Desired output: "{\"title\": \"Docs\"}"
    lines = response.split('\n')
    # Skip first line (```json) and last line (```) if present
    response = '\n'.join(lines[1:-1] if lines[-1].strip() == '```' else lines[1:])
```

### Inline Comments Guide

#### When to Comment
✅ **Comment these:**
- Non-obvious logic ("Why" not "What")
- Workarounds for bugs/limitations
- Performance optimizations
- Security-sensitive code
- Magic numbers/constants

❌ **Don't comment these:**
- Self-explanatory code
- Already described by function docstring
- Obvious variable names

#### Examples

**Good:**
```python
# Gemini sometimes returns markdown despite JSON-only prompt
response = response.replace('```json', '').replace('```', '').strip()

# Rate limiting: Free tier allows 15 req/min, we add 2s delay for safety
time.sleep(self.request_delay)

# Limit context to 100K chars to stay within Gemini's 1M token limit
# Rough estimate: 1 token ≈ 4 chars, so 100K chars ≈ 25K tokens
context = context[:100000]
```

**Bad:**
```python
# Set temperature to 0.7
temperature = 0.7

# Loop through sections
for section in sections:
    # Generate content
    content = generate(section)
```

---

## 📞 Support & Resources

### Internal Resources
- **This File:** `/home/user/Desktop/documentation_generator/claude.md`
- **Global Guidelines:** `/home/user/Downloads/global_claude_md.md`
- **User Guide:** `project_readme.md`
- **Setup Instructions:** `setup_guide_gemini.md`

### External Resources
- **Gemini API Docs:** https://ai.google.dev/docs
- **python-docx Docs:** https://python-docx.readthedocs.io/
- **Selenium Docs:** https://www.selenium.dev/documentation/
- **Repomix GitHub:** https://github.com/yamadashy/repomix

### Getting Help
```bash
# 1. Check error message carefully
python run_doc_generator.py 2>&1 | tee error.log

# 2. Review configuration
cat .env | grep -v "^#" | grep -v "^$"

# 3. Test dependencies
python -c "import google.generativeai; import selenium; print('OK')"

# 4. Check API key validity
curl -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
  "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-pro:generateContent?key=YOUR_API_KEY"

# 5. Consult this file (claude.md) troubleshooting section
```

---

## 📝 Maintenance

### Regular Updates
- **Monthly:** Review Gemini API changelog for breaking changes
- **Quarterly:** Update dependencies (`pip list --outdated`)
- **As Needed:** Update this file when architecture changes

### Keeping claude.md Updated
```bash
# When making architectural changes:
# 1. Update relevant sections in claude.md
# 2. Commit documentation with code changes
git add doc_generator.py claude.md
git commit -m "feat(export): add PDF export support

- Implemented PDFExporter class
- Updated DocumentationGenerator to support --format=pdf
- Documented in claude.md architecture section"

# When adding new features:
# 3. Update "Future Enhancements" → move to "Completed"
# 4. Add to "Usage Workflows" if user-facing
```

### Version History
- **v1.0.0** (Initial): Basic FastAPI structure (deprecated)
- **v2.0.0** (2025-10-09): Complete Gemini-based generator
  - Switched from planned FastAPI to standalone Python script
  - Implemented GeminiDocAgent, ScreenshotAgent, DocumentAssembler
  - Added .env-based configuration
  - Created comprehensive documentation suite

---

## 🎓 Learning Resources

### For New Contributors

#### Understanding the Codebase
```bash
# 1. Read in this order:
cat project_readme.md          # High-level overview
cat setup_guide_gemini.md      # Setup process
cat claude.md                  # This file - deep dive
cat doc_generator.py           # Source code

# 2. Trace execution flow:
python doc_generator.py
# Debugger: python -m pdb doc_generator.py
# Or add: import pdb; pdb.set_trace()
```

#### Key Concepts to Understand
1. **Gemini API:** Generative AI for text generation
   - Sends prompt → receives markdown text
   - JSON mode for structured data (documentation plan)
   - Rate limits and error handling

2. **Selenium WebDriver:** Browser automation
   - Render HTML → capture screenshot
   - Headless mode (no visible browser window)
   - Wait strategies (time-based, element-based)

3. **python-docx:** Word document manipulation
   - Programmatically create .docx files
   - Add headings, paragraphs, images, tables
   - Style management (fonts, colors, sizes)

4. **Repomix:** Codebase consolidation
   - Crawls project directory
   - Combines all files into single text file
   - Preserves structure and file metadata

---

## 🏁 Quick Start Checklist

### First-Time Setup
- [ ] Clone/download project to `/home/user/Desktop/documentation_generator`
- [ ] Install Python 3.8+ (`python --version`)
- [ ] Create virtual environment (`python -m venv venv`)
- [ ] Activate venv (`source venv/bin/activate`)
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Get Gemini API key from https://aistudio.google.com/apikey
- [ ] Copy `.env.example` to `.env` (if template exists)
- [ ] Edit `.env` with your API key and project path
- [ ] Test: `python run_doc_generator.py`
- [ ] Verify: `ls output/documentation.docx`

### Per-Project Usage
- [ ] (Optional) Generate repomix for project: `repomix /path/to/project -o repomix.txt`
- [ ] Copy repomix file to doc generator folder (if used)
- [ ] Update `.env` with project-specific settings
- [ ] (Optional) Start app if capturing live screenshots
- [ ] Run: `python run_doc_generator.py`
- [ ] Review output: `libreoffice output/documentation.docx`
- [ ] Edit as needed (Gemini generates 80-90% complete docs)
- [ ] Export to PDF if needed (File → Export as PDF in LibreOffice)

---

**Last Updated:** 2025-10-09
**Maintained By:** Project developer (update with your name/team)
**Questions?** Reference global guidelines at `/home/user/Downloads/global_claude_md.md`
