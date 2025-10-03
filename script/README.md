# Shell Scripts for Brain33 Project

I'll create professional shell scripts for your Brain33 project. Here are the scripts:

## 1. [Download Words Script](/download_words.sh) 
## 2. [Install Dependencies Script](/install_dependencies.sh)
## 3. [Main Setup Script](/setup_brain33.sh)


### Download Words Script Documentation

**File Location:** `/script/download_words.sh`

**Purpose:**
This script downloads the [`Words.txt`](https://github.com/Pymmdrza/Brain33/releases/download/Words/Words.txt) file from the Brain33 GitHub repository releases and saves it to the project root directory.

**Features:**
- Automatically detects the project root directory regardless of execution location
- Supports both curl and wget for downloading
- Provides colored output for better readability
- Includes file existence check with user confirmation for overwrite
- Verifies successful download with file size display
- Error handling for missing download tools

**Usage:**
```bash
cd /path/to/project
bash script/download_words.sh
```

**Requirements:**
- curl or wget must be installed
- Internet connection

**Output:**
- Downloads Words.txt to the project root directory
- Displays download progress and completion status

---

### Install Dependencies Script Documentation

**File Location:** `/script/install_dependencies.sh`

**Purpose:**
Installs all required Python packages for the Brain33 project with multiple installation methods for compatibility.

**Features:**
- Checks for pip3 availability before installation
- Displays Python and pip versions
- Attempts three different installation methods for each package:
  1. Standard installation
  2. Installation with `--break-system-packages` flag
  3. Installation with `--user` flag
- Provides colored output for installation status
- Displays comprehensive installation summary
- Lists failed packages with manual installation commands

**Required Packages:**
- rich
- libcrypto
- requests-random-user-agent

**Usage:**
```bash
bash script/install_dependencies.sh
```

**Requirements:**
- Python3
- pip3

---

### Main Setup Script Documentation

**File Location:** `/script/setup_brain33.sh`

**Purpose:**
Complete setup script that clones the [Brain33](https://github.com/Pymmdrza/Brain33) repository and installs all required dependencies.

**Features:**
- Checks for required system tools (git, python3, pip3)
- Clones the Brain33 repository from GitHub
- Handles existing directory with user confirmation
- Automatically installs pip3 if missing
- Calls `install_dependencies.sh` for package installation
- Provides fallback manual installation if install script is missing
- Comprehensive error handling and status messages
- Returns to original directory after completion

**Usage:**
```bash
bash setup_brain33.sh
```

**Requirements:**
- git
- Python3
- pip3 (will be installed if missing)
- Internet connection
- Debian-based Linux distribution (Ubuntu, Debian, etc.)

**Process Flow:**
1. Verify system requirements
2. Clone Brain33 repository
3. Install Python dependencies
4. Display completion status and usage instructions

---

### Making Scripts Executable

After creating these scripts, make them executable:

```bash
chmod +x script/download_words.sh
chmod +x script/install_dependencies.sh
chmod +x script/setup_brain33.sh
```

