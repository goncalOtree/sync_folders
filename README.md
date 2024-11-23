# Sync Program

A simple folder synchronization utility that that synchronizes two folders: source and replica. The program maintains a full, identical copy of source folder at replica folder. The program logs the process and errors in a log file.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Logging](#logging)
- [Testing](#testing)

## Installation

1. Clone the repository:

   ```bash
   git clone [https://github.com/goncalOtree/sync_folders.git]
   cd sync_folders
   ```

## Usage

The program accepts the following command-line arguments:

- `<source_folder>`: The path to the source folder.
- `<replica_folder>`: The path to the replica folder.
- `<log_file>`: The path to the log file.
- `--i INTERVAL`: The time interval (in seconds) between synchronizations. Defaults to `60` if not provided.

To run the program, use the following command:

```bash
python main.py <source_folder> <replica_folder> <log_file> [--i INTERVAL]
```

### Example Command

```bash
python main.py /Users/username/source /Users/username/replica /Users/username/sync_log.log --i 90
```

This will sync the source and replica folders every 90 seconds and log the activity to `sync_log.log`.

## Logging

The program logs synchronization activities, such as updated/removed/created files and skipped files with corresponding error (e.g., `PermissionError`, `FileNotFoundError`). The log file is specified by the user in the command line and is created if it does not already exist.

Example log entry:

```txt
2024-11-23 12:34:56,789 - INFO - Updated "/path/to/replica_folder/file1.txt"
2024-11-23 12:35:01,234 - WARNING - Skipped file "/path/to/source_folder/restricted.txt": [Errno 13] Permission denied: '/path/to/source_folder/restricted.txt'
```

## Testing

### Requirements

You can run tests using `pytest`:

1. Install `pytest` if you haven't already:

   ```bash
   pip install pytest
   ```

2. Run the tests:

   ```bash
   pytest test_sync.py
   ```

