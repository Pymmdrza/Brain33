#!/bin/bash

# Script: setup_brain33.sh
# Description: Main setup script for Brain33 project
# Usage: Run this script to clone the repository and install all dependencies
# Requirements: git, Python3, and pip3 must be installed

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Repository details
REPO_OWNER="Pymmdrza"
REPO_NAME="Brain33"
REPO_URL="https://github.com/$REPO_OWNER/$REPO_NAME.git"

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}Brain33 Project Setup${NC}"
echo -e "${CYAN}========================================${NC}"
echo

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed${NC}"
    echo -e "${YELLOW}Please install git first:${NC}"
    echo -e "  sudo apt update"
    echo -e "  sudo apt install git -y"
    exit 1
fi

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python3 is not installed${NC}"
    echo -e "${YELLOW}Please install Python3 first:${NC}"
    echo -e "  sudo apt update"
    echo -e "  sudo apt install python3 python3-pip -y"
    exit 1
fi

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 is not installed${NC}"
    echo -e "${YELLOW}Installing pip3...${NC}"
    sudo apt update
    sudo apt install python3-pip -y
fi

# Get current directory
CURRENT_DIR="$(pwd)"

# Check if Brain33 directory already exists
if [ -d "$REPO_NAME" ]; then
    echo -e "${YELLOW}Warning: $REPO_NAME directory already exists${NC}"
    read -p "Do you want to remove it and clone again? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Removing existing directory...${NC}"
        rm -rf "$REPO_NAME"
    else
        echo -e "${YELLOW}Using existing directory...${NC}"
        cd "$REPO_NAME"
        echo -e "${YELLOW}Pulling latest changes...${NC}"
        git pull
        cd "$CURRENT_DIR"
    fi
fi

# Clone repository if it doesn't exist
if [ ! -d "$REPO_NAME" ]; then
    echo -e "${BLUE}Cloning repository from GitHub...${NC}"
    echo -e "Repository: ${GREEN}$REPO_URL${NC}"
    echo
    git clone "$REPO_URL"
    echo
    echo -e "${GREEN}Repository cloned successfully${NC}"
fi

# Change to project directory
cd "$REPO_NAME"
PROJECT_ROOT="$(pwd)"
echo -e "Project directory: ${GREEN}$PROJECT_ROOT${NC}"
echo

# Install dependencies
echo -e "${BLUE}========================================${NC}"
echo -e "Installing Dependencies"
echo -e "${BLUE}========================================${NC}"
echo

# Check if install_dependencies.sh exists
if [ -f "script/install_dependencies.sh" ]; then
    echo -e "${GREEN}Running install_dependencies.sh...${NC}"
    bash script/install_dependencies.sh
else
    echo -e "${YELLOW}Warning: script/install_dependencies.sh not found${NC}"
    echo -e "${YELLOW}Installing dependencies manually...${NC}"
    
    # Manual installation
    PACKAGES=(
        "rich"
        "libcrypto"
        "requests"
        "requests-random-user-agent"
    )
    
    for package in "${PACKAGES[@]}"; do
        echo -e "${YELLOW}Installing $package...${NC}"
        if pip3 install "$package" 2>/dev/null || pip3 install "$package" --break-system-packages 2>/dev/null; then
            echo -e "${GREEN}  $package installed successfully${NC}"
        else
            echo -e "${RED}  Failed to install $package${NC}"
        fi
    done
fi

echo
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Setup Complete${NC}"
echo -e "${BLUE}========================================${NC}"
echo
echo -e "${GREEN}Brain33 project is ready to use${NC}"
echo -e "Project location: ${GREEN}$PROJECT_ROOT${NC}"
echo
echo -e "${CYAN}To run the project:${NC}"
echo -e "  cd $REPO_NAME"
echo -e "  python3 brain33_V5.py"
echo

# Return to original directory
cd "$CURRENT_DIR"
cd "$REPO_NAME"
# run 
python3 brain33_V5.py
