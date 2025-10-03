
## Download Words Script

- [Download_Words.sh](https://raw.githubusercontent.com/Pymmdrza/Brain33/refs/heads/mainx/script/download_words.sh 'Download Script Alphabet words from release') downloads the `Words.txt` file from the GitHub release to the project root directory.

### Location

The script is located at: `/script/download_words.sh`

### Functionality

The script performs the following operations:

1. Determines the project root directory relative to the script location
2. Downloads the Words.txt file from the GitHub release using curl
3. Saves the file to the project root directory
4. Provides feedback on download progress and completion
5. Handles errors during the download process

### Usage

Run the script from any location:

```bash
bash script/download_words.sh
```

Or make it executable and run directly:

```bash
chmod +x script/download_words.sh
./script/download_words.sh
```

### Requirements

- `curl` command must be available on the system
- Write permissions to the project root directory
- Internet connection to access GitHub releases

### Output

The downloaded file will be saved to: `<project_root>/Words.txt`

### Error Handling

The script will exit with an error message if:

- curl is not installed
- Download fails
- File cannot be written to the destination

### Features

- Fast and efficient download using curl
- Automatic project root detection
- Progress indicator during download
- Error checking and user feedback
- Cross-platform compatibility (Linux, macOS, Unix-like systems)
