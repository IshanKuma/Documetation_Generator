#!/usr/bin/env python3
"""
Wrapper Script for Documentation Generator
===========================================

This script validates the environment and configuration before running the main
documentation generator. It provides helpful error messages and setup guidance.

Purpose:
    - Check if .env file exists (create template if missing)
    - Validate required environment variables are set
    - Verify Python dependencies are installed
    - Display configuration summary
    - Run the main generator with error handling

Usage:
    python run_doc_generator.py

Author: Documentation Generator Team
Last Updated: 2025-10-09
"""

from dotenv import load_dotenv
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple


load_dotenv(override=True)


# ANSI color codes for terminal output (makes errors/success messages stand out)
class Colors:
    """Terminal color codes for better user experience."""
    HEADER = '\033[95m'      # Purple/magenta for headers
    OKBLUE = '\033[94m'      # Blue for info messages  
    OKCYAN = '\033[96m'      # Cyan for highlights
    OKGREEN = '\033[92m'     # Green for success messages
    WARNING = '\033[93m'     # Yellow for warnings
    FAIL = '\033[91m'        # Red for errors
    ENDC = '\033[0m'         # Reset to default color
    BOLD = '\033[1m'         # Bold text
    UNDERLINE = '\033[4m'    # Underlined text


def print_header(text: str) -> None:
    """
    Print a formatted header with decorative borders.
    
    Args:
        text (str): Header text to display
        
    Example:
        print_header("Starting Generator")
        # Outputs:
        # ╔═══════════════════════════════════════╗
        # ║      Starting Generator               ║
        # ╚═══════════════════════════════════════╝
    """
    width = 60
    print(f"\n{Colors.BOLD}╔{'═' * (width - 2)}╗{Colors.ENDC}")
    print(f"{Colors.BOLD}║{text.center(width - 2)}║{Colors.ENDC}")
    print(f"{Colors.BOLD}╚{'═' * (width - 2)}╝{Colors.ENDC}\n")


def check_env_file() -> Tuple[bool, Dict[str, str]]:
    """
    Check if .env file exists and is properly configured.
    
    This function:
    1. Checks if .env file exists in current directory
    2. If missing, creates a template .env file with all required settings
    3. If exists, loads and parses environment variables
    4. Returns success status and loaded config
    
    Returns:
        Tuple[bool, Dict[str, str]]: (success, config_dict)
            - success: True if .env exists and is readable
            - config_dict: Dictionary of environment variables
            
    Side Effects:
        - Creates .env file if it doesn't exist
        - Prints error messages and instructions if problems found
    """
    env_file = Path('.env')
    
    # Case 1: .env file doesn't exist → create template
    if not env_file.exists():
        print(f"{Colors.FAIL}❌ .env file not found!{Colors.ENDC}\n")
        print(f"{Colors.WARNING}📝 Creating template .env file...{Colors.ENDC}")
        
        # Template content with explanatory comments
        template = """# ==========================================
# Documentation Generator Configuration
# ==========================================

# Google Gemini API Configuration
# Get your free API key from: https://aistudio.google.com/apikey
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-pro

# Project Configuration
PROJECT_NAME=My Project
PROJECT_PATH=/absolute/path/to/your/project
PROJECT_DESCRIPTION=Brief project description

# Repomix Configuration (Optional - for better context)
USE_REPOMIX=false
REPOMIX_FILE_PATH=./repomix-output.txt

# Output Configuration
OUTPUT_DIRECTORY=./output
OUTPUT_FILENAME=documentation.docx
SCREENSHOTS_DIRECTORY=./screenshots

# Screenshot Configuration
ENABLE_SCREENSHOTS=true
BROWSER_CHOICE=chrome
SCREENSHOT_WAIT_TIME=3

# Live Application Screenshots (Optional)
LIVE_APP_ENABLED=false
LIVE_APP_URL_HOME=http://localhost:3000

# Advanced Settings
MAX_CODE_BLOCK_LINES=50
MAX_FILE_SIZE_KB=100
EXCLUDED_DIRECTORIES=node_modules,.git,__pycache__,venv,.venv,dist,build

# Gemini API Settings
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_OUTPUT_TOKENS=8000
GEMINI_REQUEST_DELAY=2
"""
        
        # Write template to .env file
        with open(env_file, 'w') as f:
            f.write(template)
        
        print(f"{Colors.OKGREEN}✓ Created .env file{Colors.ENDC}\n")
        print(f"{Colors.BOLD}📋 Next steps:{Colors.ENDC}")
        print(f"  1. Edit .env file with your settings")
        print(f"  2. Get Gemini API key from: {Colors.OKCYAN}https://aistudio.google.com/apikey{Colors.ENDC}")
        print(f"  3. Update PROJECT_PATH to your project location")
        print(f"  4. Run this script again\n")
        
        return False, {}
    
    # Case 2: .env exists → load and parse
    config = {}
    try:
        with open(env_file, 'r') as f:
            for line in f:
                # Skip comments and empty lines
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parse KEY=VALUE pairs
                if '=' in line:
                    key, value = line.split('=', 1)  # Split only on first =
                    config[key.strip()] = value.strip()
        
        return True, config
    
    except Exception as e:
        print(f"{Colors.FAIL}❌ Error reading .env file: {e}{Colors.ENDC}")
        return False, {}


def validate_config(config: Dict[str, str]) -> List[str]:
    """
    Validate that all required configuration values are present and valid.
    
    Checks:
    - GEMINI_API_KEY is set and not placeholder
    - PROJECT_NAME is set
    - PROJECT_PATH is set and exists (directory)
    - Output directories are writable
    - Browser choice is valid
    
    Args:
        config (Dict[str, str]): Configuration dictionary from .env
        
    Returns:
        List[str]: List of error messages. Empty list = all valid.
        
    Example:
        errors = validate_config(config)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
    """
    errors = []
    
    # Required: API Key
    api_key = config.get('GEMINI_API_KEY', '')
    if not api_key or api_key == 'your_api_key_here':
        errors.append("GEMINI_API_KEY is not set or is still the placeholder")
        errors.append("  → Get your free API key from: https://aistudio.google.com/apikey")
    
    # Required: Project Name
    if not config.get('PROJECT_NAME'):
        errors.append("PROJECT_NAME is not set")
        errors.append("  → Set a descriptive name for your project")
    
    # Required: Project Path (must be absolute and exist)
    project_path = config.get('PROJECT_PATH', '')
    if not project_path:
        errors.append("PROJECT_PATH is not set")
        errors.append("  → Set the absolute path to your project directory")
    elif not os.path.isabs(project_path):
        errors.append(f"PROJECT_PATH must be absolute path, got: {project_path}")
        errors.append(f"  → Use absolute paths like: /home/user/my-project")
    elif not os.path.exists(project_path):
        errors.append(f"PROJECT_PATH does not exist: {project_path}")
        errors.append(f"  → Verify the path and fix typos")
    elif not os.path.isdir(project_path):
        errors.append(f"PROJECT_PATH is not a directory: {project_path}")
    
    # Optional but validated if set: Browser choice
    browser = config.get('BROWSER_CHOICE', 'chrome').lower()
    if browser not in ['chrome', 'firefox']:
        errors.append(f"Invalid BROWSER_CHOICE: {browser}")
        errors.append("  → Must be 'chrome' or 'firefox'")
    
    # Validate repomix if enabled
    if config.get('USE_REPOMIX', 'false').lower() == 'true':
        repomix_path = config.get('REPOMIX_FILE_PATH', './repomix-output.txt')
        if not os.path.exists(repomix_path):
            errors.append(f"USE_REPOMIX=true but file not found: {repomix_path}")
            errors.append("  → Generate with: repomix /path/to/project -o repomix-output.txt")
            errors.append("  → Or set USE_REPOMIX=false to scan directory instead")
    
    return errors


def check_dependencies() -> List[str]:
    """
    Check if all required Python packages are installed.
    
    Attempts to import each required package and returns list of missing ones.
    This is faster than pip freeze and gives us exactly what we need.
    
    Returns:
        List[str]: List of missing package names. Empty = all installed.
        
    Implementation Note:
        Uses __import__() instead of actual imports to avoid side effects
        and to handle packages with different import names vs pip names.
    """
    # Map of import names to pip package names (some differ!)
    required_packages = {
        'google.generativeai': 'google-generativeai',  # Import name ≠ pip name
        'dotenv': 'python-dotenv',                     # Import name ≠ pip name
        'docx': 'python-docx',                         # Import name ≠ pip name
        'selenium': 'selenium',                        # Import name = pip name
        'webdriver_manager': 'webdriver-manager',      # Import name ≠ pip name
        'PIL': 'Pillow',                               # Import name ≠ pip name
    }
    
    missing = []
    
    for import_name, pip_name in required_packages.items():
        try:
            # Try to import the module
            # __import__() dynamically imports without executing module code
            __import__(import_name)
        except ImportError:
            # Package not installed
            missing.append(pip_name)
    
    return missing


def display_config_summary(config: Dict[str, str]) -> None:
    """
    Display a nicely formatted summary of the current configuration.
    
    Shows key settings that affect documentation generation so user can
    verify everything is correct before running (saves time if misconfigured).
    
    Args:
        config (Dict[str, str]): Configuration dictionary from .env
        
    Output:
        Prints formatted table to terminal with key settings
    """
    print(f"{Colors.BOLD}📋 Configuration:{Colors.ENDC}")
    print("─" * 60)
    
    # Define which settings to show and their display names
    important_settings = [
        ('PROJECT_NAME', 'Project Name'),
        ('PROJECT_PATH', 'Project Path'),
        ('USE_REPOMIX', 'Use Repomix'),
        ('REPOMIX_FILE_PATH', 'Repomix File'),
        ('OUTPUT_DIRECTORY', 'Output Dir'),
        ('ENABLE_SCREENSHOTS', 'Screenshots'),
        ('BROWSER_CHOICE', 'Browser'),
        ('LIVE_APP_ENABLED', 'Live App'),
        ('GEMINI_MODEL', 'Gemini Model'),
    ]
    
    # Print each setting with consistent formatting
    for key, label in important_settings:
        value = config.get(key, 'Not set')
        # Truncate long paths for readability
        if len(value) > 50:
            value = '...' + value[-47:]
        print(f"{label:<20}: {Colors.OKCYAN}{value}{Colors.ENDC}")
    
    print("─" * 60 + "\n")


def main() -> int:
    """
    Main entry point for the wrapper script.
    
    Orchestrates the entire validation and execution flow:
    1. Print welcome banner
    2. Check .env file exists
    3. Validate configuration
    4. Check Python dependencies
    5. Display config summary
    6. Prompt for live app if needed
    7. Run main generator
    8. Handle errors gracefully
    
    Returns:
        int: Exit code (0 = success, 1 = error)
        
    Flow:
        Success: Display output location and next steps
        Failure: Show clear error message and how to fix
    """
    # Welcome banner
    print_header("Automated Documentation Generator v2.0")
    print(f"{Colors.BOLD}     Powered by Google Gemini 2.5 Pro{Colors.ENDC}")
    print()
    
    # Step 1: Check .env file
    print(f"{Colors.BOLD}🔍 Checking configuration...{Colors.ENDC}")
    env_exists, config = check_env_file()
    
    if not env_exists:
        # .env was just created, exit so user can edit it
        return 1
    
    # Step 2: Validate configuration
    validation_errors = validate_config(config)
    
    if validation_errors:
        print(f"{Colors.FAIL}❌ Configuration errors found:{Colors.ENDC}\n")
        for error in validation_errors:
            print(f"  {error}")
        print(f"\n{Colors.WARNING}Please fix the errors in .env and try again.{Colors.ENDC}\n")
        return 1
    
    print(f"{Colors.OKGREEN}✓ Configuration validated{Colors.ENDC}\n")
    
    # Step 3: Check dependencies
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"{Colors.FAIL}❌ Missing required packages:{Colors.ENDC}\n")
        for package in missing_packages:
            print(f"  - {package}")
        print(f"\n{Colors.BOLD}Install with:{Colors.ENDC}")
        print(f"  pip install {' '.join(missing_packages)}")
        print(f"\n{Colors.BOLD}Or install all dependencies:{Colors.ENDC}")
        print(f"  pip install -r requirements.txt\n")
        return 1
    
    # Step 4: Display configuration summary
    display_config_summary(config)
    
    # Step 5: Check if live app screenshots are enabled
    if config.get('LIVE_APP_ENABLED', 'false').lower() == 'true':
        print(f"{Colors.WARNING}⚠️  Live app screenshots are enabled{Colors.ENDC}")
        print(f"{Colors.BOLD}Make sure your application is running before proceeding.{Colors.ENDC}\n")
        
        # Collect all LIVE_APP_URL_* variables
        live_urls = {k: v for k, v in config.items() if k.startswith('LIVE_APP_URL_')}
        
        if live_urls:
            print(f"{Colors.BOLD}URLs to capture:{Colors.ENDC}")
            for key, url in live_urls.items():
                name = key.replace('LIVE_APP_URL_', '').lower()
                print(f"  - {name}: {Colors.OKCYAN}{url}{Colors.ENDC}")
            print()
        
        # Prompt user to confirm app is running
        response = input(f"{Colors.BOLD}Is your app running? (y/n): {Colors.ENDC}").strip().lower()
        if response != 'y':
            print(f"\n{Colors.WARNING}Exiting. Start your app and run again.{Colors.ENDC}\n")
            return 1
        print()
    
    # Step 6: Initialize and run the main generator
    print(f"{Colors.BOLD}🔧 Initializing generator...{Colors.ENDC}")
    
    try:
        # Import the main generator module
        # We import here (not at top) so validation happens first
        from doc_generator import DocumentationGenerator
        
        # Create generator instance (loads .env internally)
        generator = DocumentationGenerator()
        
        # Run the generation pipeline
        output_path = generator.generate()

        # Create completion marker file to signal successful completion
        # This is especially useful in Docker containers to detect when generation is done
        output_dir = Path(os.getenv('OUTPUT_DIRECTORY', './output'))
        completion_marker = output_dir / '.complete'
        try:
            with open(completion_marker, 'w') as f:
                f.write(f"Documentation generation completed successfully\n")
                f.write(f"Generated: {output_path}\n")
                f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            print(f"\n✓ Completion marker created: {completion_marker}")
        except Exception as e:
            print(f"⚠️  Could not create completion marker: {e}")

        # Success!
        return 0
        
    except KeyboardInterrupt:
        # User pressed Ctrl+C
        print(f"\n\n{Colors.WARNING}⚠️  Generation interrupted by user{Colors.ENDC}\n")
        return 1
        
    except Exception as e:
        # Unexpected error occurred
        print(f"\n{Colors.FAIL}❌ Error during generation:{Colors.ENDC}")
        print(f"  {str(e)}\n")
        
        # Show stack trace for debugging
        import traceback
        print(f"{Colors.WARNING}Stack trace:{Colors.ENDC}")
        traceback.print_exc()
        print()
        
        return 1


# Entry point when script is run directly
if __name__ == "__main__":
    sys.exit(main())
