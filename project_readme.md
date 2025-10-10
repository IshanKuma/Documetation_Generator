# 📚 Automated Documentation Generator

> Generate comprehensive technical documentation for your projects using Google Gemini AI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4)](https://ai.google.dev/)

## ✨ Features

- 🤖 **AI-Powered**: Uses Google Gemini 2.0 Flash (FREE with generous limits)
- 📄 **Word Documents**: Creates professional `.docx` files
- 📸 **Automated Screenshots**: Captures code files and directory structure
- 🌐 **Live App Capture**: Screenshots of your running application
- ⚙️ **Simple Configuration**: Everything in `.env` file
- 🚀 **Zero Cost**: Completely free to use
- 📦 **Local Processing**: All files stored locally

## 🎯 What It Does

1. **Analyzes** your codebase (via repomix or directory scan)
2. **Generates** comprehensive documentation structure
3. **Captures** screenshots of code files and running app
4. **Creates** professional Word document with:
   - Overview & Architecture
   - Installation & Setup
   - Core Components
   - API Reference
   - Usage Examples
   - Configuration Guide
   - Development Guide
   - Troubleshooting

## 🚀 Quick Start

### 1. Setup (5 minutes)

```bash
# Clone or create directory
mkdir doc-automation && cd doc-automation

# Download files (doc_generator.py and run_doc_generator.py)
# Or use setup script:
chmod +x setup.sh && ./setup.sh
```

### 2. Get FREE Gemini API Key

1. Visit: https://aistudio.google.com/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

### 3. Configure

```bash
# Edit .env file (auto-created on first run)
nano .env

# Minimum required:
GEMINI_API_KEY=AIzaSy...your-key-here
PROJECT_PATH=/path/to/your/project
PROJECT_NAME=My Awesome Project
```

### 4. Run

```bash
python run_doc_generator.py
```

**Output:** `output/documentation.docx` 🎉

## 📋 Requirements

- Python 3.8+
- Chrome browser
- Google Gemini API key (FREE)

## 📦 Installation

### Option 1: Automatic Setup

```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install google-generativeai python-dotenv python-docx selenium webdriver-manager

# Create directories
mkdir output screenshots
```

## ⚙️ Configuration (.env)

### Essential Settings

```bash
# API Key (REQUIRED)
GEMINI_API_KEY=AIzaSy...

# Project Info (REQUIRED)
PROJECT_NAME=My Project
PROJECT_PATH=/absolute/path/to/project
PROJECT_DESCRIPTION=Optional description

# Output
OUTPUT_DIRECTORY=./output
OUTPUT_FILENAME=documentation.docx
SCREENSHOTS_DIRECTORY=./screenshots
```

### Optional: Repomix (Recommended)

```bash
# Install repomix
npm install -g repomix

# Generate repomix file
cd /path/to/your/project
repomix . -o repomix-output.txt

# Copy to doc-automation
cp repomix-output.txt /path/to/doc-automation/

# Enable in .env
USE_REPOMIX=true
REPOMIX_FILE_PATH=./repomix-output.txt
```

### Optional: Live App Screenshots

```bash
# Enable live app capture
LIVE_APP_ENABLED=true

# Add URLs
LIVE_APP_URL_HOME=http://localhost:3000
LIVE_APP_URL_DASHBOARD=http://localhost:3000/dashboard
LIVE_APP_URL_API=http://localhost:8000/docs
```

## 📖 Usage Examples

### Basic Usage

```bash
python run_doc_generator.py
```

### With Live App Screenshots

```bash
# Terminal 1: Start your app
cd /path/to/project
npm start  # or python manage.py runserver

# Terminal 2: Generate docs
cd doc-automation
python run_doc_generator.py
# When prompted, type: y
```

### Fast Mode (No Screenshots)

```bash
# In .env: ENABLE_SCREENSHOTS=false
python run_doc_generator.py
```

## 📁 Project Structure

```
doc-automation/
├── doc_generator.py           # Main generator
├── run_doc_generator.py       # Runner script
├── .env                       # Configuration
├── requirements.txt           # Dependencies
├── setup.sh                   # Setup script
├── output/                    # Generated docs
│   └── documentation.docx
└── screenshots/               # Captured images
    ├── src_main.py.png
    └── directory_structure.png
```

## 🔧 Troubleshooting

### "GEMINI_API_KEY not found"
- Check `.env` file exists
- Verify no spaces around `=`
- Make sure key starts with `AIza`

### "Project path does not exist"
- Use absolute paths: `/home/user/project`
- Not relative: `~/project` or `../project`

### "Screenshots are blank"
- Increase wait time: `SCREENSHOT_WAIT_TIME=5`
- Try Firefox: `BROWSER_CHOICE=firefox`

### "Rate limit exceeded"
- Increase delay: `GEMINI_REQUEST_DELAY=5`
- Free tier: 15 requests/minute

## 💰 Cost

**Completely FREE!** 🎉

Gemini 2.0 Flash free tier:
- ✅ 15 requests per minute
- ✅ 1,500 requests per day
- ✅ 1M tokens/minute input
- ✅ 32K tokens/minute output

Typical usage:
- Small project: 3-5 requests
- Medium project: 8-12 requests
- Large project: 15-25 requests

**All within free tier limits!**

## 🎓 Best Practices

1. **Use Repomix**: Better context = better docs
   ```bash
   repomix /path/to/project -o repomix.txt
   ```

2. **Capture Live App**: Show real UI
   ```bash
   LIVE_APP_ENABLED=true
   ```

3. **Exclude Unnecessary Directories**:
   ```bash
   EXCLUDED_DIRECTORIES=node_modules,.git,venv,dist
   ```

4. **Review and Edit**: Generated docs are 80-90% complete
   - Add company-specific details
   - Verify technical accuracy
   - Add internal links

## 🆚 Why Gemini vs Claude?

| Feature | Gemini 2.0 Flash | Claude Sonnet 4.5 |
|---------|------------------|-------------------|
| **Cost** | ✅ FREE | ❌ $3-15 per 1M tokens |
| **Rate Limits** | ✅ 1500/day | ❌ Lower on free tier |
| **Quality** | ✅ Excellent | ✅ Excellent |
| **API Key** | ✅ No credit card | ⚠️ Requires payment method |
| **Setup** | ✅ Instant | ⚠️ Waitlist for API |

**Winner: Gemini** for this use case! 🏆

## 📊 Example Output

Generated documentation includes:

1. **Title Page** with project name and description
2. **Overview** - What the project does
3. **Architecture** - System design and components
4. **Installation** - Step-by-step setup
5. **Core Components** - Deep dive into modules
6. **API Reference** - Endpoints and usage
7. **Usage Examples** - Code samples
8. **Configuration** - Environment variables
9. **Development Guide** - Contributing guidelines
10. **Troubleshooting** - Common issues

With embedded:
- 📸 Code screenshots
- 📸 Directory structure
- 📸 Live app screenshots
- 💻 Code blocks
- 📝 Professional formatting

## 🤝 Contributing

Contributions welcome! This is a lightweight tool designed to be simple and effective.

Areas for improvement:
- Additional export formats (PDF, Markdown)
- Custom templates
- More screenshot types
- Better error handling

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Credits

- **Powered by**: Google Gemini 2.0 Flash
- **Browser Automation**: Selenium
- **Document Generation**: python-docx
- **Codebase Consolidation**: Repomix

## 💡 Tips

- **First time?** Use repomix for best results
- **Web app?** Enable live screenshots
- **Multiple projects?** Create separate `.env` files
- **CI/CD?** Easy to integrate (see docs)
- **Questions?** Check the complete setup guide

---

**Made with ❤️ by developers, for developers**

Get started: `python run_doc_generator.py`
