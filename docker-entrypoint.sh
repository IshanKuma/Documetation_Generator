#!/bin/bash
# ==========================================
# Docker Entrypoint Script
# ==========================================
# Purpose: Fix volume mount permission issues
# This script runs BEFORE the main application starts
#
# Problem it solves:
# - When volumes are mounted from the host, they may have wrong ownership/permissions
# - The container runs as user 'docgen' (UID 1000) but mounted dirs may be owned by root or host user
# - This causes "Permission denied" errors when trying to write to these directories
#
# Solution:
# - Ensure all required directories exist
# - Ensure they are writable by the current user (docgen)
# - If running as root (for debugging), create with proper permissions

set -e  # Exit on error

echo "🔧 Docker entrypoint: Checking directory permissions..."

# Directories that need to be writable
REQUIRED_DIRS=(
    "/app/output"
    "/app/screenshots"
    "/app/mermaid_diagrams"
)

# Function to ensure directory exists and is writable
ensure_writable_dir() {
    local dir="$1"

    # Create directory if it doesn't exist
    if [ ! -d "$dir" ]; then
        echo "  📁 Creating directory: $dir"
        mkdir -p "$dir" 2>/dev/null || {
            echo "  ⚠️  Could not create $dir (may need to run as root or check volume mount)"
        }
    fi

    # Test if writable by creating and removing a test file
    if [ -d "$dir" ]; then
        local test_file="$dir/.write_test_$$"
        if touch "$test_file" 2>/dev/null; then
            rm -f "$test_file"
            echo "  ✓ $dir is writable"
        else
            echo "  ⚠️  $dir exists but is NOT writable"
            echo "     This may cause errors during documentation generation"
            echo "     Fix: Run 'chmod 777 $(realpath $dir 2>/dev/null || echo $dir)' on the host"
        fi
    fi
}

# Check each required directory
for dir in "${REQUIRED_DIRS[@]}"; do
    ensure_writable_dir "$dir"
done

echo "✓ Directory permission check complete"
echo ""

# Execute the main command (CMD from Dockerfile)
# "$@" passes all arguments to this script (which is the CMD)
exec "$@"
