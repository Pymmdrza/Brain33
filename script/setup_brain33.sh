#!/bin/bash

# Script: setup_brain33.sh
# Description: Main setup script for Brain33 project
# Author: Pymmdrza
# Usage: ./setup_brain33.sh

git clone https://github.com/Pymmdrza/Brain33
cd Brain33
sudo apt install python3-venv -y&&python3 -m venv venv&&source venv/bin/activate
venv/bin/pip install libcrypto rich requests requests-random-user-agent
chmod +x script/*.sh
script/download_addr.sh
venv/bin/python Brain33_V5.py Words.txt
