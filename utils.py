import os
from hashlib import md5
import shutil
from pathlib import Path

def calculate_md5(filename):
    with open(filename, 'rb') as f:
        digest = md5(f.read()).hexdigest()
    return digest

def exists_path(path):
    if not Path(path).exists():
        return False
    return True

def is_dir(dirname):
    if not Path(dirname).is_dir():
        return False
    return True

def create_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def remove_dir(path):
    Path(path).rmdir()

def copy_file(src_path,rep_path):
    shutil.copy2(src_path,rep_path)

def remove_file(path):
    Path(path).unlink()

def get_relpath(file,src,rep):
    return os.path.join(rep, Path(file).relative_to(src))

def compare_files(file1,file2):
    return calculate_md5(file1) == calculate_md5(file2)

def get_files_from_dir(dirname):
    files_to_sync = []
    for path, folders, files in os.walk(dirname):
        for folder in folders:
            files_to_sync.append(os.path.join(path, folder))
        for file in files:
            files_to_sync.append(os.path.join(path, file))
    return files_to_sync




 