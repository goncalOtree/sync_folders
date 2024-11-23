import os
import shutil
import logging
from pathlib import Path
import pytest
from sync import sync

@pytest.fixture
def setup_test_environment(tmp_path):
    """
    Create a temporary test environment with source and replica folders.
    """

    logs = tmp_path / "logs.log"

    # Clear existing handlers and reconfigure
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)


    logging.basicConfig(filename=logs, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    source = tmp_path /  "source_folder"
    replica = tmp_path / "replica_folder"

    # Create directories
    source.mkdir()
    replica.mkdir()

    # Add some test files to the source
    (source / "file1.txt").write_text("This is file 1")
    (source / "file2.txt").write_text("This is file 2")
    (source / "subdir").mkdir()
    (source / "subdir" / "file3.txt").write_text("This is file 3 in subdir")

    return source, replica, logger

def test_sync_basic_functionality(setup_test_environment):
    """
    Test basic synchronization from source to replica.
    """
    source, replica, logger = setup_test_environment

    # Run sync
    sync(source, replica, logger)

    # Check that files are copied
    assert (replica / "file1.txt").read_text() == "This is file 1"
    assert (replica / "file2.txt").read_text() == "This is file 2"
    assert (replica / "subdir" / "file3.txt").read_text() == "This is file 3 in subdir"

def test_sync_updates(setup_test_environment):
    """
    Test that updated files in the source are synced to the replica.
    """
    source, replica, logger = setup_test_environment

    sync(source, replica, logger)

    # Update a file in the source
    (source / "file1.txt").write_text("Updated content for file 1")

    # Resync
    sync(source, replica, logger)

    # Check updated content
    assert (replica / "file1.txt").read_text() == "Updated content for file 1"

def test_remove_files(setup_test_environment):
    """
    Test that files removed from the source are also removed from the replica.
    """
    source, replica, logger = setup_test_environment

    # Remove a file from the source
    (source / "file2.txt").unlink()
   
    sync(source, replica, logger)

    # Check that the file is removed in the replica
    assert not (replica / "file2.txt").exists()

def test_sync_empty_directories(setup_test_environment):
    """
    Test handling of empty directories.
    """
    source, replica, logger = setup_test_environment

    # Add an empty directory in the source
    empty_dir = source / "empty_dir"
    empty_dir.mkdir()

    sync(source, replica, logger)

    # Check that the empty directory exists in the replica
    assert (replica / "empty_dir").is_dir()

def test_sync_nonexistent_source(setup_test_environment):
    """
    Test behavior when the source folder does not exist.
    """

    _,_,logger = setup_test_environment

    source = Path("/nonexistent/source")
    replica = Path("/tmp/replica")

    with pytest.raises(FileNotFoundError):
        sync(source, replica, logger)

def test_sync_creates_replica(setup_test_environment):
    """
    Test that the replica folder is created if it doesn't exist.
    """
    source, replica, logger = setup_test_environment

    # Delete the replica folder
    shutil.rmtree(replica)

    sync(source, replica, logger)

    # Check that the replica folder is recreated
    assert replica.exists()

def test_file_conflict_resolution(setup_test_environment):
    """Test handling of files with the same name but different content."""
    source, replica, logger = setup_test_environment

    # Create a file in the source and replica with the same name but different contents
    (source / "conflict.txt").write_text("Source content")
    (replica / "conflict.txt").write_text("Replica content")

    sync(source, replica, logger)

    # Assert the replica file was overwritten by the source file
    assert (replica / "conflict.txt").read_text() == "Source content"


def test_large_files(setup_test_environment):
    """Test synchronization of large files."""
    source, replica, logger = setup_test_environment

    # Create a large file in the source
    large_file = source / "large_file.txt"
    large_file.write_bytes(b"A" * 10**6)  # 1 MB file

    sync(source, replica, logger)

    # Assert the large file was copied correctly
    assert (replica / "large_file.txt").exists()
    assert (replica / "large_file.txt").stat().st_size == large_file.stat().st_size


def test_deeply_nested_directories(setup_test_environment):
    """Test synchronization of deeply nested directories."""
    source, replica, logger = setup_test_environment

    # Create a deeply nested directory structure in the source
    nested_dir = source / "a" / "b" / "c" / "d"
    nested_dir.mkdir(parents=True)
    (nested_dir / "nested_file.txt").write_text("Nested content")

    sync(source, replica, logger)

    # Assert the nested structure exists in the replica
    assert (replica / "a" / "b" / "c" / "d" / "nested_file.txt").exists()


def test_interval_logic(mocker, setup_test_environment):
    """Test synchronization respects the specified interval."""
    import time

    source, replica, logger = setup_test_environment

    # Mock the sleep function to simulate intervals without delay
    mocker.patch("time.sleep")

    (source / "file1.txt").write_text("Content")
    sync(source, replica, logger)

    (source / "file2.txt").write_text("New Content")

    time.sleep(300)  # Simulate a 5-minute interval
    sync(source, replica, logger)

    # Assert that both files are now in the replica
    assert (replica / "file1.txt").exists()
    assert (replica / "file2.txt").exists()


def test_file_permissions(setup_test_environment, tmp_path):
    """
    Test error handling for files restricted permissions
    """
    source, replica, logger = setup_test_environment

    logs = tmp_path / "logs.log"

    (source / "restricted.txt").write_text("Restricted content new")
    (replica / "restricted.txt").write_text("Restricted content")
    
    # Restrict permissions
    os.chmod(replica / "restricted.txt",0o000)

    sync(source, replica, logger)

    # Read logs
    with open(logs) as log_file:
        log_contents = log_file.read()
        assert "Skipped file" in log_contents

    # Return to normal permissions 
    os.chmod(replica / "restricted.txt",0o644)


