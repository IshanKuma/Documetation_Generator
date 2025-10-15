#!/bin/bash
# ==========================================
# Docker Volume Directory Setup Script
# ==========================================
# Purpose: Create host directories for Docker volume mounts with correct permissions
#
# Why this is needed:
# - Docker volume mounts inherit permissions from the host directory
# - If directories don't exist, Docker creates them as root-owned
# - Container runs as user 'docgen' (UID 1000) and can't write to root-owned dirs
# - This script creates directories with permissions that allow container writes
#
# Usage:
#   chmod +x setup-docker-dirs.sh
#   ./setup-docker-dirs.sh
#
# Or run directly:
#   bash setup-docker-dirs.sh

set -e  # Exit on error

echo "🔧 Setting up Docker volume directories..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Directories to create (relative to script location)
DIRS=(
    "output"
    "screenshots"
    "mermaid_diagrams"
)

# Function to create directory with proper permissions
create_dir() {
    local dir="$1"

    if [ -d "$dir" ]; then
        echo "  ✓ $dir already exists"
        # Ensure it's writable
        chmod 755 "$dir" 2>/dev/null || {
            echo "    ⚠️  Could not set permissions on $dir (may need sudo)"
        }
    else
        echo "  📁 Creating $dir"
        mkdir -p "$dir"
        chmod 755 "$dir"
        echo "  ✓ Created $dir with permissions 755"
    fi
}

# Create each directory
for dir in "${DIRS[@]}"; do
    create_dir "$dir"
done

echo ""
echo "✅ Directory setup complete!"
echo ""
echo "📋 Created directories:"
echo "   - ./output/           (for generated documentation)"
echo "   - ./screenshots/      (for captured screenshots)"
echo "   - ./mermaid_diagrams/ (for architecture diagrams)"
echo ""
echo "🚀 You can now run: docker compose up"
echo ""
