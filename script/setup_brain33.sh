#!/bin/bash

# Script: setup.sh
# Description: Main setup script for Brain33 project
# Author: Pymmdrza
# Usage: ./setup.sh

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Script files
DOWNLOAD_SCRIPT="$SCRIPT_DIR/download_words.sh"
INSTALL_SCRIPT="$SCRIPT_DIR/install_dependencies.sh"

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}     Brain33 Setup Script v1.0         ${NC}"
echo -e "${CYAN}========================================${NC}"
echo

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed${NC}"
    echo "Please install git first:"
    echo "  sudo apt update"
    echo "  sudo apt install git -y"
    exit 1
fi

# Step 1: Grant execution permissions to scripts
echo -e "${BLUE}[Step 1/4] Setting execution permissions for scripts...${NC}"
if [ -f "$DOWNLOAD_SCRIPT" ] && [ -f "$INSTALL_SCRIPT" ]; then
    chmod +x "$DOWNLOAD_SCRIPT"
    chmod +x "$INSTALL_SCRIPT"
    chmod +x "$0"
    echo -e "${GREEN}Permissions granted successfully${NC}"
else
    echo -e "${RED}Error: Required scripts not found${NC}"
    echo "Expected locations:"
    echo "  - $DOWNLOAD_SCRIPT"
    echo "  - $INSTALL_SCRIPT"
    exit 1
fi
echo

# Step 2: Clone repository if not already cloned
echo -e "${BLUE}[Step 2/4] Checking Brain33 repository...${NC}"
if [ -d "$PROJECT_ROOT/.git" ]; then
    echo -e "${YELLOW}Repository already exists, updating...${NC}"
    cd "$PROJECT_ROOT"
    git pull origin main || git pull origin master || echo -e "${YELLOW}Could not update repository${NC}"
else
    echo -e "${GREEN}Cloning Brain33 repository...${NC}"
    REPO_URL="https://github.com/Pymmdrza/Brain33.git"
    TEMP_DIR="${PROJECT_ROOT}_temp"
    
    git clone "$REPO_URL" "$TEMP_DIR"
    
    # Move contents to project root
    if [ -d "$TEMP_DIR" ]; then
        cp -r "$TEMP_DIR"/* "$PROJECT_ROOT/" 2>/dev/null || true
        cp -r "$TEMP_DIR"/.* "$PROJECT_ROOT/" 2>/dev/null || true
        rm -rf "$TEMP_DIR"
        echo -e "${GREEN}Repository cloned successfully${NC}"
    else
        echo -e "${RED}Error: Failed to clone repository${NC}"
        exit 1
    fi
fi
echo

# Step 3: Install packages
echo -e "${BLUE}[Step 3/4] Installing required packages...${NC}"
if bash "$INSTALL_SCRIPT"; then
    echo -e "${GREEN}Packages installed successfully${NC}"
else
    echo -e "${RED}Warning: Some packages failed to install${NC}"
    echo -e "${YELLOW}You may need to install them manually${NC}"
fi
echo

# Step 4: Download Words.txt
echo -e "${BLUE}[Step 4/4] Downloading Words.txt file...${NC}"
if bash "$DOWNLOAD_SCRIPT"; then
    echo -e "${GREEN}Words.txt downloaded successfully${NC}"
else
    echo -e "${RED}Warning: Failed to download Words.txt${NC}"
    echo -e "${YELLOW}You may need to download it manually${NC}"
fi
echo

# Final summary
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}     Setup Complete!                    ${NC}"
echo -e "${CYAN}========================================${NC}"
echo
echo -e "${GREEN}Project root: $PROJECT_ROOT${NC}"
echo -e "${GREEN}All setup tasks completed${NC}"
echo
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Navigate to project root: cd $PROJECT_ROOT"
echo "  2. Run the main script or application"
echo
echo -e "${BLUE}For more information, visit:${NC}"
echo "  https://github.com/Pymmdrza/Brain33"
echo

exit 0
