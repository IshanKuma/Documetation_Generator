
# Documentation Generator - Complete Setup Guide
## Gemini-Powered, .env Configured

---

## 🎯 Overview

This tool automatically generates comprehensive technical documentation for your project using:
- ✅ **Google Gemini 2.0 Flash** (FREE API with generous limits)
- ✅ **Selenium** for automated screenshots
- ✅ **python-docx** for Word document generation
- ✅ **All configuration in .env file** (no JSON configs)

---

## 📋 Prerequisites

- Python 3.8 or higher
- Chrome browser (already installed)
- Google Gemini API key (free)

---

## 🚀 Complete Setup (Step-by-Step)

### Step 1: Get Your Free Gemini API Key

1. Go to **https://aistudio.google.com/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIza...`)

**No credit card required! Free tier includes:**
- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per minute

---

### Step 2: Create Project Directory

```bash
# Create main directory
mkdir doc-automation
cd doc-automation

# Create subdirectories
mkdir output screenshots
```

**Directory structure:**
```
doc-automation/
├── doc_generator.py       # Main generator script
├── run_doc_generator.py   # Runner script
├── .env                   # Configuration (auto-generated)
├── requirements.txt       # Dependencies
├── output/                # Generated docs go here
└── screenshots/           # Screenshots saved here
```

---

### Step 3: Install Dependencies

**Create `requirements.txt`:**
```bash
cat > requirements.txt << 'EOF'
google-generativeai>=0.3.0
python-dotenv>=1.0.0
python-docx>=1.1.0
selenium>=4.16.0
webdriver-manager>=4.0.1
Pillow>=10.0.0
EOF
```

**Install everything:**
```bash
# Recommended: Use virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**What gets installed:**
- `google-generativeai` - Gemini API client (FREE)
- `python-dotenv` - Load .env files
- `python-docx` - Create Word documents
- `selenium` - Browser automation
- `webdriver-manager` - Auto-manages Chrome driver

---

### Step 4: Download Project Files

Save these files to `doc-automation/`:

1. **`doc_generator.py`** - Main generator (from artifacts above)
2. **`run_doc_generator.py`** - Runner script (from artifacts above)

**Quick download (if you have the files):**
```bash
# Assuming files are in current directory
cp doc_generator.py doc-automation/
cp run_doc_generator.py doc-automation/
```

---

### Step 5: First Run (Auto-generates .env)

```bash
cd doc-automation
python run_doc_generator.py
```

**This will create a template `.env` file automatically!**

Output:
```
❌ .env file not found!

📝 Creating template .env file...
✓ Created .env file

📋 Next steps:
  1. Edit .env file with your settings
  2. Get Gemini API key from: https://aistudio.google.com/apikey
  3. Update PROJECT_PATH to your project location
  4. Run this script again
```

---

### Step 6: Configure .env File

**Edit `.env` with your settings:**

```bash
# Open in your favorite editor
nano .env
# or
code .env
# or
vim .env
```

**Minimal Configuration (Required):**
```bash
# API Key (REQUIRED)
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Project Settings (REQUIRED)
PROJECT_NAME=My Awesome Project
PROJECT_PATH=/home/user/my-project
PROJECT_DESCRIPTION=A modern web application built with React and Python

# Output Locations
OUTPUT_DIRECTORY=./output
OUTPUT_FILENAME=documentation.docx
SCREENSHOTS_DIRECTORY=./screenshots

# Features
ENABLE_SCREENSHOTS=true
BROWSER_CHOICE=chrome
```

**Full Configuration (All Options):**
```bash
# ==========================================
# API Configuration
# ==========================================
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
GEMINI_MODEL=gemini-2.0-flash-exp
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_OUTPUT_TOKENS=8000
GEMINI_REQUEST_DELAY=2

# ==========================================
# Project Configuration
# ==========================================
PROJECT_NAME=E-Commerce Platform
PROJECT_PATH=/home/user/projects/ecommerce
PROJECT_DESCRIPTION=Full-stack e-commerce platform with React frontend and Django backend

# ==========================================
# Repomix Configuration (RECOMMENDED)
# ==========================================
# Generate with: repomix /path/to/project -o repomix-output.txt
USE_REPOMIX=true
REPOMIX_FILE_PATH=./repomix-output.txt

# ==========================================
# Output Configuration
# ==========================================
OUTPUT_DIRECTORY=./output
OUTPUT_FILENAME=technical_documentation.docx
SCREENSHOTS_DIRECTORY=./screenshots

# ==========================================
# Screenshot Configuration
# ==========================================
ENABLE_SCREENSHOTS=true
BROWSER_CHOICE=chrome
SCREENSHOT_WAIT_TIME=3
MAX_CODE_BLOCK_LINES=50

# ==========================================
# Live Application Screenshots (Optional)
# ==========================================
# Set LIVE_APP_ENABLED=true to capture running app
LIVE_APP_ENABLED=false
LIVE_APP_URL_HOME=http://localhost:3000
LIVE_APP_URL_DASHBOARD=http://localhost:3000/dashboard
LIVE_APP_URL_ADMIN=http://localhost:3000/admin
LIVE_APP_URL_API_DOCS=http://localhost:8000/docs

# Add more URLs as needed:
# LIVE_APP_URL_LOGIN=http://localhost:3000/login
# LIVE_APP_URL_PROFILE=http://localhost:3000/profile

# ==========================================
# Advanced Settings
# ==========================================
MAX_FILE_SIZE_KB=100
EXCLUDED_DIRECTORIES=node_modules,.git,__pycache__,venv,.venv,dist,build,.next,coverage
```

---

### Step 7: (Optional) Generate Repomix File

**For best results, use repomix to consolidate your codebase:**

```bash
# Install repomix globally
npm install -g repomix

# Generate repomix file for your project
cd /path/to/your/project
repomix . -o repomix-output.txt

# Copy to doc-automation directory
cp repomix-output.txt /path/to/doc-automation/

# Update .env
# USE_REPOMIX=true
# REPOMIX_FILE_PATH=./repomix-output.txt
```

**Why use repomix?**
- ✅ Consolidates entire codebase into one file
- ✅ Better context for Gemini
- ✅ More accurate documentation
- ✅ Fewer API calls = faster generation

---

### Step 8: Run the Generator!

```bash
cd doc-automation
python run_doc_generator.py
```

**Expected output:**
```
╔═══════════════════════════════════════════════════════════╗
║     Automated Documentation Generator v2.0                ║
║     Powered by Google Gemini 2.0 Flash                    ║
╚═══════════════════════════════════════════════════════════╝

🔍 Checking configuration...
✓ Configuration validated

📋 Configuration:
────────────────────────────────────────────────────────────
Project Name    : My Awesome Project
Project Path    : /home/user/my-project
Use Repomix     : true
Repomix File    : ./repomix-output.txt
Output Dir      : ./output
Screenshots     : true
Browser         : Chrome
Live App        : false
Gemini Model    : gemini-2.0-flash-exp
────────────────────────────────────────────────────────────

🔧 Initializing generator...
✓ Initialized Gemini model: gemini-2.0-flash-exp
✓ Screenshot directory: /path/to/doc-automation/screenshots
✓ Output will be saved to: /path/to/doc-automation/output/documentation.docx

============================================================
🚀 Starting documentation generation for: My Awesome Project
============================================================

📖 Phase 1: Loading project context...
✓ Loaded 45231 characters from repomix

📋 Phase 2: Creating documentation plan...
✓ Created plan with 9 sections:
  1. Overview
  2. Architecture & Design
  3. Installation & Setup
  4. Core Components
  5. API Reference
  6. Usage Examples
  7. Configuration
  8. Development Guide
  9. Troubleshooting

✍️  Phase 3: Generating content...
  [1/9] Generating: Overview
      📸 Capturing 1 screenshots...
  [2/9] Generating: Architecture & Design
      📸 Capturing 2 screenshots...
  [3/9] Generating: Installation & Setup
  [4/9] Generating: Core Components
      📸 Capturing 3 screenshots...
  [5/9] Generating: API Reference
  [6/9] Generating: Usage Examples
      📸 Capturing 2 screenshots...
  [7/9] Generating: Configuration
  [8/9] Generating: Development Guide
  [9/9] Generating: Troubleshooting
✓ Content generation complete

📄 Phase 4: Assembling Word document...
✅ Documentation saved to: /path/to/output/documentation.docx

============================================================
✅ Documentation generation complete!
============================================================

📄 Document: /path/to/doc-automation/output/documentation.docx
📸 Screenshots: /path/to/doc-automation/screenshots

💡 Next steps:
  1. Open the .docx file in Word/Google Docs/LibreOffice
  2. Review and edit as needed
  3. Share with your team!
```

---

## 📊 .env Configuration Reference

### Essential Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Your Gemini API key | `AIzaSy...` | ✅ Yes |
| `PROJECT_NAME` | Your project name | `My App` | ✅ Yes |
| `PROJECT_PATH` | Absolute path to project | `/home/user/project` | ✅ Yes |

### File Locations (All paths relative to script location)

| Variable | Description | Default | Purpose |
|----------|-------------|---------|---------|
| `OUTPUT_DIRECTORY` | Where docs are saved | `./output` | Generated .docx location |
| `SCREENSHOTS_DIRECTORY` | Where screenshots saved | `./screenshots` | Screenshot storage |
| `REPOMIX_FILE_PATH` | Repomix file location | `./repomix-output.txt` | Consolidated codebase |

### Screenshot Settings

| Variable | Options | Default | Description |
|----------|---------|---------|-------------|
| `ENABLE_SCREENSHOTS` | `true`/`false` | `true` | Enable/disable screenshots |
| `BROWSER_CHOICE` | `chrome`/`firefox` | `chrome` | Browser for screenshots |
| `SCREENSHOT_WAIT_TIME` | Number (seconds) | `3` | Wait before capturing |

### Live App Screenshots

To capture screenshots of your running application:

```bash
# Enable live app screenshots
LIVE_APP_ENABLED=true

# Define URLs (add as many as needed)
LIVE_APP_URL_HOME=http://localhost:3000
LIVE_APP_URL_DASHBOARD=http://localhost:3000/dashboard
LIVE_APP_URL_API=http://localhost:8000/docs
LIVE_APP_URL_ADMIN=http://localhost:8000/admin
# Add more: LIVE_APP_URL_XXX=http://...
```

**When running with live app:**
1. Start your application first
2. Run `python run_doc_generator.py`
3. Script will prompt: "Is your app running? (y/n)"
4. Type `y` and press Enter

---

## 🎯 Usage Examples

### Example 1: Basic Documentation (No Repomix)

**Scenario:** Quick documentation without repomix

**.env:**
```bash
GEMINI_API_KEY=AIzaSyXXX...
PROJECT_NAME=Simple API
PROJECT_PATH=/home/user/simple-api
USE_REPOMIX=false
ENABLE_SCREENSHOTS=true
```

**Run:**
```bash
python run_doc_generator.py
```

Generator will scan your project directory automatically.

---

### Example 2: Best Quality (With Repomix)

**Scenario:** Comprehensive documentation with full codebase context

**Steps:**
```bash
# 1. Generate repomix
cd /home/user/my-project
repomix . -o repomix.txt

# 2. Copy to doc-automation
cp repomix.txt /path/to/doc-automation/repomix-output.txt

# 3. Update .env
# USE_REPOMIX=true
# REPOMIX_FILE_PATH=./repomix-output.txt

# 4. Run generator
cd /path/to/doc-automation
python run_doc_generator.py
```

---

### Example 3: With Live Application Screenshots

**Scenario:** Capture screenshots of running web app

**.env:**
```bash
GEMINI_API_KEY=AIzaSyXXX...
PROJECT_NAME=Web Dashboard
PROJECT_PATH=/home/user/dashboard
LIVE_APP_ENABLED=true
LIVE_APP_URL_HOME=http://localhost:3000
LIVE_APP_URL_ANALYTICS=http://localhost:3000/analytics
LIVE_APP