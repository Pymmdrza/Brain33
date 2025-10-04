#!/bin/bash

# Script: setup_brain33.sh
# Description: Main setup script for Brain33 project
# Author: Pymmdrza
# Usage: ./setup_brain33.sh

git clone https://github.com/Pymmdrza/Brain33
cd Brain33
chmod +x script/*.sh
script/install_dependencies.sh
script/download_words.sh
