#!/bin/bash

# Script: download_words.sh
# Description: Downloads the Words.txt file from Brain33 repository releases
# Usage: Run this script from any location within the project
# Output: Words.txt file will be saved in the project root directory

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the project root directory (one level up from script directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# File URL and destination
FILE_URL="https://github.com/Pymmdrza/Rich-Address-Wallet/releases/download/Bitcoin/Latest_Rich_Bitcoin_P2PKH.txt.gz"
DEST_FILE="$PROJECT_ROOT/Words.txt.gz"

echo -e "${YELLOW}Starting download process...${NC}"
echo -e "Project Root: ${GREEN}$PROJECT_ROOT${NC}"
echo -e "Destination: ${GREEN}$DEST_FILE${NC}"

# Check if file already exists
if [ -f "$DEST_FILE" ]; then
    echo -e "${YELLOW}Warning: Words.txt already exists in the project root${NC}"
    read -p "Do you want to overwrite it? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Download cancelled by user${NC}"
        exit 1
    fi
fi

# Download the file using curl or wget
if command -v curl &> /dev/null; then
    echo -e "${GREEN}Downloading with curl...${NC}"
    curl -L -o "$DEST_FILE" "$FILE_URL" --progress-bar
elif command -v wget &> /dev/null; then
    echo -e "${GREEN}Downloading with wget...${NC}"
    wget -O "$DEST_FILE" "$FILE_URL"
else
    echo -e "${RED}Error: Neither curl nor wget is installed${NC}"
    echo -e "${YELLOW}Please install curl or wget and try again${NC}"
    exit 1
fi

# Verify download
if [ -f "$DEST_FILE" ] && [ -s "$DEST_FILE" ]; then
    FILE_SIZE=$(du -h "$DEST_FILE" | cut -f1)
    echo -e "${GREEN}Download completed successfully${NC}"
    echo -e "File size: ${GREEN}$FILE_SIZE${NC}"
    echo -e "Location: ${GREEN}$DEST_FILE${NC}"
    gunzip $DEST_FILE
    echo -e "Un Zip file successfully in : $PROJECT_ROOT"
else
    echo -e "${RED}Error: Download failed or file is empty${NC}"
    exit 1
fi
