#!/bin/bash

#########################################################
# Words.txt Downloader Script
# Description: Downloads Words.txt file from GitHub releases
# Author: Professional Shell Script
# Date: 2025-10-03
#########################################################

set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Exit on pipe failure

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Configuration
readonly DOWNLOAD_URL="https://github.com/Pymmdrza/Brain33/releases/download/Words/Words.txt"
readonly FILE_NAME="Words.txt"

# Get the project root directory (one level up from script directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
readonly TARGET_PATH="${PROJECT_ROOT}/${FILE_NAME}"

#########################################################
# Functions
#########################################################

# Print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Download using curl
download_with_curl() {
    print_info "Using curl for download..."
    curl -L --progress-bar --fail --retry 3 --retry-delay 2 \
         --max-time 300 -o "${TARGET_PATH}" "${DOWNLOAD_URL}"
}

# Download using wget
download_with_wget() {
    print_info "Using wget for download..."
    wget --progress=bar:force --tries=3 --timeout=300 \
         -O "${TARGET_PATH}" "${DOWNLOAD_URL}"
}

# Main download function
download_file() {
    print_info "Starting download process..."
    print_info "Source: ${DOWNLOAD_URL}"
    print_info "Target: ${TARGET_PATH}"
    print_info "Project Root: ${PROJECT_ROOT}"
    
    # Check if file already exists
    if [[ -f "${TARGET_PATH}" ]]; then
        print_warning "File already exists: ${TARGET_PATH}"
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Download cancelled by user."
            exit 0
        fi
        print_info "Removing existing file..."
        rm -f "${TARGET_PATH}"
    fi
    
    # Try curl first, then wget
    if command_exists curl; then
        download_with_curl
    elif command_exists wget; then
        download_with_wget
    else
        print_error "Neither curl nor wget is available!"
        print_error "Please install one of them: sudo apt-get install curl"
        exit 1
    fi
    
    # Verify download
    if [[ -f "${TARGET_PATH}" && -s "${TARGET_PATH}" ]]; then
        local file_size=$(du -h "${TARGET_PATH}" | cut -f1)
        print_success "Download completed successfully!"
        print_success "File location: ${TARGET_PATH}"
        print_success "File size: ${file_size}"
        
        # Display first few lines as verification
        print_info "First 5 lines of the file:"
        head -n 5 "${TARGET_PATH}" 2>/dev/null || true
    else
        print_error "Download failed or file is empty!"
        rm -f "${TARGET_PATH}" 2>/dev/null || true
        exit 1
    fi
}

# Cleanup on error
cleanup() {
    if [[ $? -ne 0 ]]; then
        print_error "An error occurred during download!"
        if [[ -f "${TARGET_PATH}" ]]; then
            print_info "Cleaning up incomplete download..."
            rm -f "${TARGET_PATH}" 2>/dev/null || true
        fi
    fi
}

#########################################################
# Main Execution
#########################################################

# Set trap for cleanup
trap cleanup EXIT

# Print banner
echo "=========================================="
echo "  Words.txt Download"
echo "  Brain33 Project - Pymmdrza"
echo "=========================================="
echo

# Run download
download_file

print_success "All done! ✓"
exit 0
