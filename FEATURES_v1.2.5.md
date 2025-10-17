# Documentation Generator - New Features v1.2.5

## Summary
This release adds several critical features to enhance the professional quality and usability of generated documentation.

---

## ✨ New Features

### 1. **Table of Contents (TOC)** 📑
- **Location**: Automatically inserted after the cover page, before all sections
- **Features**:
  - Hierarchical section listing with proper indentation
  - Professional formatting with section numbers
  - Clear visual hierarchy (Level 1 sections in bold)
  - Instructions for page number updates in Word/LibreOffice
- **Implementation**: `DocumentAssembler.add_table_of_contents()` method
- **Benefits**: Improved navigation for large documents, professional appearance

### 2. **Hyperlinks and References** 🔗
- **Auto-Detection**: Automatically detects and converts URLs to clickable hyperlinks
- **Supported Formats**:
  - `https://` URLs
  - `http://` URLs
  - `www.` URLs (automatically prefixed with http://)
- **Features**:
  - Clickable links in generated Word documents
  - Blue color with underline styling (standard hyperlink appearance)
  - Works alongside markdown formatting (bold, italic)
- **AI Integration**: Gemini now encouraged to include relevant URLs for:
  - Official documentation
  - GitHub repositories
  - API references
  - Framework homepages
  - Standards and specifications
- **Implementation**: `DocumentAssembler._add_hyperlink()` method with XML manipulation

### 3. **Contributors and Authors List** 👥
- **Location**: Cover page (after project description and date)
- **New Environment Variables**:
  - `DOCUMENTATION_AUTHOR`: Single author/lead name
  - `DOCUMENTATION_CONTRIBUTORS`: Comma-separated list of contributors
  - `DOCUMENTATION_ORGANIZATION`: Company/organization name (with © symbol)
- **Format**:
  - **Author**: Displays as "Author: [Name]"
  - **Contributors**: Formatted as bulleted list with heading
  - **Organization**: Displays as "© [Organization Name]"
- **Example**:
  ```
  Contributors
  • Claude AI
  • Development Team
  • Project Manager

  © Your Organization Name
  ```

### 4. **PDF Export Enabled** 📄
- **Status**: Now enabled by default (`ENABLE_PDF_EXPORT=true`)
- **Supported Methods**:
  - **python-docx2pdf** (Windows): Best quality, native Word rendering
  - **LibreOffice** (Cross-platform): Excellent quality, widely available
  - Comprehensive error messages with installation instructions
- **Benefits**: Single command generates both .docx and .pdf formats
- **Files Updated**:
  - `.env`: `ENABLE_PDF_EXPORT=true`
  - `docker-compose.yml`: `ENABLE_PDF_EXPORT=true`

### 5. **Mermaid Diagram Improvements** 🎨
- **Enhanced Error Handling**:
  - Better ChromeDriver/Puppeteer compatibility detection
  - Automatic Chrome/Chromium path detection in Docker
  - Clearer error messages with actionable suggestions
- **Size Optimization**:
  - Reduced max diagram size to 1500 chars (from 2000)
  - More aggressive Gemini prompts for minimal diagrams
  - Maximum 5-7 nodes (down from 8-10)
  - Enforced 500-character limit in prompts
- **Improved Prompts**:
  - Emphasized simplicity and brevity
  - Better examples showing good vs bad diagrams
  - Explicit character count limits
- **Fallback Handling**:
  - Better detection of "URI Too Long" errors
  - Saves Mermaid code to .txt with link to https://mermaid.live/
  - Clear instructions for manual rendering
- **Docker Support**:
  - Auto-detects Chromium paths: `/usr/bin/chromium`, `/usr/bin/chromium-browser`, `/usr/bin/google-chrome`
  - Sets `PUPPETEER_EXECUTABLE_PATH` environment variable

---

## 🔧 Technical Changes

### Code Modifications

#### 1. `doc_generator.py`
- **New Methods**:
  - `DocumentAssembler.add_table_of_contents(sections)`: Generates TOC page
  - `DocumentAssembler._add_hyperlink(paragraph, url, text)`: Adds clickable hyperlink using XML
  - Enhanced `DocumentAssembler._add_formatted_paragraph(text)`: Now detects and converts URLs

- **Enhanced Methods**:
  - `DocumentAssembler.add_title_page()`: Now includes contributors and organization
  - `MermaidAgent.render_diagram()`: Improved error handling and size checks
  - `MermaidAgent.generate_diagram_code()`: More aggressive size constraints
  - `GeminiDocAgent.generate_section_content()`: Updated prompt to include URLs

- **Enhanced Prompts**:
  - Section generation: Encourages including relevant URLs and references
  - Diagram generation: Stricter size limits and simplicity requirements

#### 2. `.env` File
- Added `DOCUMENTATION_AUTHOR=AI Documentation Team`
- Added `DOCUMENTATION_CONTRIBUTORS=Claude AI, Development Team`
- Added `DOCUMENTATION_ORGANIZATION=Your Organization Name`
- Changed `ENABLE_PDF_EXPORT=false` → `ENABLE_PDF_EXPORT=true`

#### 3. `docker-compose.yml`
- Added `DOCUMENTATION_AUTHOR` environment variable
- Added `DOCUMENTATION_CONTRIBUTORS` environment variable
- Added `DOCUMENTATION_ORGANIZATION` environment variable
- Changed `ENABLE_PDF_EXPORT=false` → `ENABLE_PDF_EXPORT=true`

---

## 📋 Configuration

### New Environment Variables

```bash
# Documentation Metadata (Optional)
DOCUMENTATION_AUTHOR=AI Documentation Team
DOCUMENTATION_CONTRIBUTORS=Claude AI, Development Team, Project Manager
DOCUMENTATION_ORGANIZATION=Your Organization Name
```

### Updated Settings

```bash
# PDF Export (now enabled by default)
ENABLE_PDF_EXPORT=true
```

---

## 🚀 Usage Examples

### Example 1: Basic Usage with New Features
```bash
# 1. Configure .env with new variables
nano .env

# Add:
DOCUMENTATION_AUTHOR=John Doe
DOCUMENTATION_CONTRIBUTORS=John Doe, Jane Smith, Bob Johnson
DOCUMENTATION_ORGANIZATION=Acme Corporation

# 2. Run generator
python run_doc_generator.py

# 3. Output includes:
#    - Cover page with contributors list
#    - Table of Contents (page 2)
#    - Sections with clickable hyperlinks
#    - Both .docx and .pdf formats
```

### Example 2: Docker Usage
```bash
# 1. Edit docker-compose.yml environment variables
nano docker-compose.yml

# 2. Run container
docker-compose up

# 3. Check output directory for:
#    - documentation.docx (with TOC, hyperlinks, contributors)
#    - documentation.pdf (if LibreOffice available)
```

---

## 🐛 Fixed Issues

### Mermaid Diagram Errors (from user report)
**Original Errors**:
```
⚠️  mmdc failed: Could not find Chrome (ver. 131.0.6778.204)
⚠️  mermaid.ink rendering failed: HTTP Error 414: URI Too Long
```

**Fixes Applied**:
1. **ChromeDriver Issue**:
   - Added automatic Chrome/Chromium detection in Docker
   - Sets `PUPPETEER_EXECUTABLE_PATH` environment variable
   - Provides clear installation instructions if not found

2. **URI Too Long Issue**:
   - Reduced diagram complexity via stricter Gemini prompts
   - Lowered size threshold from 2000 → 1500 characters
   - Added early size checks before attempting mermaid.ink
   - Better error messages with manual rendering instructions

---

## 📊 Impact Summary

| Feature | Impact | Users Affected |
|---------|--------|----------------|
| Table of Contents | High - Essential for navigation | All users |
| Hyperlinks | Medium - Improves UX | All users |
| Contributors List | High - Professional requirement | Enterprise users |
| PDF Export | High - Common requirement | 80%+ of users |
| Mermaid Fixes | High - Blocked diagram generation | Docker users |

---

## 🔄 Upgrade Instructions

### For Existing Users

1. **Pull latest code**:
   ```bash
   cd /home/user/Desktop/documentation_generator
   git pull  # If using git
   ```

2. **Update .env file**:
   ```bash
   # Add new optional variables
   echo "DOCUMENTATION_AUTHOR=Your Name" >> .env
   echo "DOCUMENTATION_CONTRIBUTORS=Team Member 1, Team Member 2" >> .env
   echo "DOCUMENTATION_ORGANIZATION=Your Company" >> .env

   # Enable PDF export
   sed -i 's/ENABLE_PDF_EXPORT=false/ENABLE_PDF_EXPORT=true/' .env
   ```

3. **Test generation**:
   ```bash
   python run_doc_generator.py
   ```

4. **Verify new features**:
   - Open generated .docx file
   - Check page 2 for Table of Contents
   - Verify cover page shows contributors
   - Click on any URLs in content
   - Check for .pdf file in output directory

### For Docker Users

1. **Update docker-compose.yml**:
   - Add new environment variables (see Configuration section)
   - Change `ENABLE_PDF_EXPORT=false` to `true`

2. **Rebuild and run**:
   ```bash
   docker-compose build
   docker-compose up
   ```

---

## 📝 Notes

### Table of Contents Limitations
- Page numbers are not automatically populated in python-docx
- Users must update page numbers manually in Word/LibreOffice:
  - Word: Right-click TOC → "Update Field"
  - LibreOffice: Tools → Update → Update All

### Hyperlink Detection
- Only detects URLs in plain text content
- Does not hyperlink URLs within code blocks
- URLs must be separated by whitespace to be detected

### PDF Export Requirements
- **Windows**: Requires python-docx2pdf + Microsoft Word
- **Linux/Docker**: Requires LibreOffice
- **macOS**: Requires LibreOffice
- Falls back gracefully if dependencies unavailable

### Mermaid Diagrams in Docker
- For best results, install Chromium in Docker:
  ```dockerfile
  RUN apt-get update && apt-get install -y chromium
  ```
- Or use online rendering via mermaid.ink (size limits apply)

---

## 🎯 Future Enhancements

Potential future improvements (not in this release):
- [ ] Dynamic TOC field codes with page numbers
- [ ] Internal cross-references between sections
- [ ] Clickable TOC entries (hyperlink to sections)
- [ ] Custom hyperlink colors/styles
- [ ] Multiple author role support (Lead, Reviewer, Editor)
- [ ] Version history tracking on cover page
- [ ] Better Mermaid rendering in Docker (bundled Chrome)

---

## 📞 Support

If you encounter issues:
1. Check error messages - they now include actionable suggestions
2. Verify environment variables are set correctly
3. For Mermaid issues: Check `mermaid_diagrams/*.txt` files
4. For PDF issues: Check if LibreOffice is installed

---

**Version**: 1.2.5
**Release Date**: 2025-10-16
**Compatibility**: Python 3.8+, Docker, Windows/Linux/macOS
