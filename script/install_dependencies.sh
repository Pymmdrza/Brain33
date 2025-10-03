#!/bin/bash

# Script: install_dependencies.sh
# Description: Installs required Python packages for Brain33 project
# Usage: Run this script to install all required dependencies
# Requirements: Python3 and pip3 must be installed

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Required packages
PACKAGES=(
    "rich"
    "libcrypto"
    "requests-random-user-agent"
)

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Brain33 Dependencies Installation${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 is not installed${NC}"
    echo -e "${YELLOW}Please Install Python3 and pip3 First${NC}"
    exit 1
fi

echo -e "${GREEN}Python Version:${NC}"
python3 --version
echo -e "${GREEN}pip3 Version:${NC}"
pip3 --version
echo

# Function to install package with different methods
install_package() {
    local package=$1
    local success=false
    
    echo -e "${YELLOW}Installing $package...${NC}"
    
    # Method 1: Standard installation
    if pip3 install "$package" &> /dev/null; then
        success=true
    # Method 2: Try with --break-system-packages flag
    elif pip3 install "$package" --break-system-packages &> /dev/null; then
        success=true
        echo -e "${YELLOW}  Installed With --break-system-packages Flag${NC}"
    # Method 3: Try with --user flag
    elif pip3 install "$package" --user &> /dev/null; then
        success=true
        echo -e "${YELLOW}  Installed With --user Flag${NC}"
    fi
    
    if [ "$success" = true ]; then
        echo -e "${GREEN}  $package Installed Successfully${NC}"
        return 0
    else
        echo -e "${RED}  Failed to Install $package${NC}"
        return 1
    fi
}

# Install all packages
failed_packages=()
for package in "${PACKAGES[@]}"; do
    if ! install_package "$package"; then
        failed_packages+=("$package")
    fi
    echo
done

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Installation Summary${NC}"
echo -e "${BLUE}========================================${NC}"

if [ ${#failed_packages[@]} -eq 0 ]; then
    echo -e "${GREEN}All Packages Installed Successfully${NC}"
    exit 0
else
    echo -e "${RED}Failed to Install the Following Packages:${NC}"
    for package in "${failed_packages[@]}"; do
        echo -e "  ${RED}- $package${NC}"
    done
    echo
    echo -e "${YELLOW}Please try Installing them Manually:${NC}"
    for package in "${failed_packages[@]}"; do
        echo -e "  pip3 install $package --break-system-packages"
    done
    exit 1
fi
