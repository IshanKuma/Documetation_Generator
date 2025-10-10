# Contributing to Documentation Generator

Thank you for your interest in contributing to the Documentation Generator project!

## 📋 Table of Contents
- [Getting Started](#getting-started)
- [Git Workflow](#git-workflow)
- [Commit Guidelines](#commit-guidelines)
- [Development Process](#development-process)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

## 🚀 Getting Started

1. **Fork & Clone**
   ```bash
   git clone <your-fork-url>
   cd documentation_generator
   ```

2. **Setup Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Setup configuration
   cp .env.example .env
   # Edit .env with your Gemini API key
   ```

3. **Verify Setup**
   ```bash
   python run_doc_generator.py
   ```

## 🌳 Git Workflow

### Branch Strategy

We follow a simple, effective branching model:

- **`master`**: Production-ready code
- **`develop`**: Integration branch for features (optional)
- **`feature/*`**: New features or enhancements
- **`fix/*`**: Bug fixes
- **`refactor/*`**: Code refactoring
- **`docs/*`**: Documentation updates

### Creating a Feature Branch

```bash
# Update master
git checkout master
git pull origin master

# Create feature branch
git checkout -b feature/add-pdf-export

# Work on your feature...

# Commit frequently (see commit guidelines below)
git add .
git commit -m "feat(export): add PDF export functionality"
```

### Branch Naming Convention

- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `refactor/what-was-refactored` - Code improvements
- `docs/what-was-documented` - Documentation changes
- `chore/task-description` - Maintenance tasks

**Examples:**
- `feature/markdown-export`
- `fix/screenshot-blank-image`
- `refactor/gemini-agent-error-handling`
- `docs/api-reference-update`

## 📝 Commit Guidelines

### Commit Message Format

We follow the **Conventional Commits** specification:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(export): add PDF export support` |
| `fix` | Bug fix | `fix(screenshot): resolve blank image issue` |
| `refactor` | Code restructuring | `refactor(gemini): improve error handling` |
| `docs` | Documentation | `docs(readme): update installation steps` |
| `style` | Code formatting | `style(generator): fix indentation` |
| `test` | Add/update tests | `test(gemini): add unit tests for API calls` |
| `chore` | Maintenance | `chore(deps): update selenium to 4.18.0` |

### Commit Scope (Optional)

Common scopes in this project:
- `init` - Initial setup
- `gemini` - Gemini agent changes
- `screenshot` - Screenshot agent changes
- `assembler` - Document assembler changes
- `config` - Configuration changes
- `export` - Export functionality
- `deps` - Dependency updates

### Good Commit Messages

✅ **Good Examples:**
```bash
feat(export): add PDF export functionality

- Implemented PDFExporter class using python-docx2pdf
- Added support for Windows and Linux/macOS
- Included error handling for missing LibreOffice

Resolves #42
```

```bash
fix(screenshot): resolve blank screenshot on slow systems

Increased default SCREENSHOT_WAIT_TIME from 3s to 5s
to allow proper page rendering on slower machines.

Fixes #38
```

```bash
refactor(gemini): improve API error handling

- Added retry logic for rate limit errors
- Better error messages for invalid API keys
- Graceful degradation when API is unavailable
```

❌ **Bad Examples:**
```bash
Update files
Fixed bug
WIP
asdf
Changed stuff
```

### When to Commit

✅ **Commit After:**
- Successfully implementing a feature
- Fixing a bug and verifying it works
- Completing a refactoring that passes tests
- **Before** risky changes (safety checkpoint)
- Every 50-100 lines of working code

⚠️ **Don't Commit:**
- Broken/non-working code
- Incomplete features (use stash instead)
- Files with secrets or API keys
- Generated files (output/, screenshots/)

## 🔧 Development Process

### Before Starting Work

1. **Create an issue** describing what you'll work on
2. **Assign yourself** to avoid duplicate work
3. **Check existing PRs** to avoid conflicts
4. **Read claude.md** for project context

### During Development

1. **Follow coding standards:**
   - Type hints required for all functions
   - Docstrings for all classes and non-trivial functions
   - Comments explaining "why", not "what"
   - Follow PEP 8 style guide

2. **Commit frequently:**
   - Small, atomic commits
   - Each commit should be working code
   - Use meaningful commit messages

3. **Test your changes:**
   - Manual testing checklist (see claude.md)
   - Verify no regressions
   - Test edge cases

4. **Update documentation:**
   - Update README if user-facing changes
   - Update claude.md if architecture changes
   - Add docstrings to new code

### Example Development Session

```bash
# 1. Create feature branch
git checkout -b feature/markdown-export

# 2. Make changes with frequent commits
# Edit code...
git add markdown_exporter.py
git commit -m "feat(export): add MarkdownExporter class skeleton"

# Edit more code...
git add markdown_exporter.py doc_generator.py
git commit -m "feat(export): integrate markdown export into generator"

# 3. Update documentation
git add README.md
git commit -m "docs(readme): document markdown export feature"

# 4. Test thoroughly
python run_doc_generator.py

# 5. Push to your fork
git push origin feature/markdown-export
```

## 🧪 Testing

### Manual Testing Checklist

Before submitting a PR, test the following:

- [ ] **Basic generation** (no repomix, no screenshots)
  ```bash
  # Set: USE_REPOMIX=false, ENABLE_SCREENSHOTS=false
  python run_doc_generator.py
  ```

- [ ] **Full generation** (with repomix and screenshots)
  ```bash
  # Set: USE_REPOMIX=true, ENABLE_SCREENSHOTS=true
  python run_doc_generator.py
  ```

- [ ] **Error handling**
  - Invalid API key
  - Missing dependencies
  - Invalid project path

- [ ] **Output validation**
  - Document opens correctly
  - Screenshots visible
  - No placeholder text
  - Proper formatting

### Future: Automated Testing

We plan to add:
- Unit tests with pytest
- Integration tests
- CI/CD pipeline
- Code coverage reporting

## 📬 Pull Request Process

### Before Submitting

1. **Update from master**
   ```bash
   git checkout master
   git pull origin master
   git checkout your-feature-branch
   git rebase master  # or merge master
   ```

2. **Verify commits**
   ```bash
   git log master..HEAD --oneline
   # Check commit messages follow conventions
   ```

3. **Self-review**
   ```bash
   git diff master
   # Review all changes carefully
   ```

4. **Update documentation**
   - README.md (if user-facing changes)
   - claude.md (if architecture changed)
   - CHANGELOG.md (if exists)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing
Describe how you tested your changes

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review performed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Manual testing completed
- [ ] Related issues linked

## Related Issues
Closes #issue_number
```

### Review Process

1. Maintainer reviews code
2. Automated checks run (future)
3. Discussion and iteration
4. Approval and merge

## 🔐 Security Guidelines

### What NOT to Commit

❌ **Never commit:**
- `.env` files with actual API keys
- Credentials or passwords
- API tokens
- SSH keys
- Database connection strings
- Repomix files with sensitive code

✅ **Safe to commit:**
- `.env.example` templates
- Public configuration
- Documentation
- Source code (without secrets)

### If You Accidentally Commit Secrets

1. **Immediately rotate** the exposed credentials
2. **Remove from git history:**
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```
3. **Notify maintainers**
4. **Never** simply delete in a new commit (history still exists)

## 📚 Additional Resources

- **Project Context:** See `claude.md`
- **User Guide:** See `project_readme.md`
- **Setup Instructions:** See `setup_guide_gemini.md`
- **Global Standards:** See `/home/user/Downloads/global_claude_md.md` (local)

## 💡 Questions?

- **Project-specific:** Open an issue
- **Git workflow:** Check `claude.md` section 🔄 Git Workflow
- **Coding standards:** Check `claude.md` section 📚 Code Documentation Standards

---

**Thank you for contributing! 🎉**

Your contributions make this project better for everyone.
