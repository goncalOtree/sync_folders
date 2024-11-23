Certainly! Below is an example of a `README.md` for your sync program. This README includes sections on setting up, using, and testing the program.

---

# Sync Program

A simple folder synchronization utility that keeps two folders in sync by copying files from the source folder to the replica folder at specified intervals. If the replica folder files differ from the source folder, the program will update them. The program logs the process and errors in a log file.

## Features
- Synchronizes files between two folders at regular intervals.
- Logs synchronization activities and errors.
- Handles errors gracefully (e.g., permission issues or file not found).
- Runs continuously, making it suitable for ongoing sync tasks.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Arguments](#arguments)
- [Logging](#logging)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/sync-program.git
   cd sync-program
   ```

2. Install the required dependencies:

   If you're using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, if you’re using a `venv`:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Usage

To run the program, use the following command:

```bash
python sync.py <source_folder> <replica_folder> <log_file> [--i INTERVAL]
```

### Example

```bash
python sync.py /path/to/source_folder /path/to/replica_folder /path/to/log_file.log --i 5
```

This will synchronize the contents of `source_folder` with `replica_folder` every 5 minutes and log the results to `log_file.log`.

## Arguments

The program accepts the following command-line arguments:

- `<source_folder>`: The path to the source folder.
- `<replica_folder>`: The path to the replica folder.
- `<log_file>`: The path to the log file.
- `--i INTERVAL`: The time interval (in minutes) between synchronizations. Defaults to `5` if not provided.

### Example Command

```bash
python sync.py /Users/username/source /Users/username/replica /Users/username/sync_log.log --i 10
```

This will sync the source and replica folders every 10 minutes and log the activity to `sync_log.log`.

## Logging

The program logs synchronization activities, such as updated files, skipped files, and any encountered errors (e.g., `PermissionError`, `FileNotFoundError`). The log file is specified by the user in the command line and is created if it does not already exist.

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
   pytest
   ```

### Test Fixtures

The tests include a fixture `setup_test_environment`, which sets up temporary folders for testing. It creates:

- `source_folder`: A folder containing test files.
- `replica_folder`: A replica folder to sync files to.
- `logs.log`: A log file where synchronization events are logged.

The tests ensure that the program handles various scenarios, including permission errors and missing files.

### Example Test

```python
def test_sync_log_creation(setup_test_environment):
    source, replica, logger, logs = setup_test_environment

    # Log a test message
    logger.info("Test log entry")

    # Verify that the log file exists and contains the log message
    assert logs.exists()
    with open(logs) as log_file:
        assert "Test log entry" in log_file.read()
```
