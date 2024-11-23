from utils import get_files_from_dir, get_relpath,exists_path,is_dir,create_dir,compare_files,copy_file,remove_dir,remove_file


def check_folders(src,rep,logger):
    """
    Confirms if the provided source and replica folders exist and are directories
    """
    if not exists_path(src):
        raise FileNotFoundError(f"Source folder not found: \"{src}\"")
    
    elif not is_dir(src):
        raise NotADirectoryError(f"Source is not a directory: \"{src}\"")
    
    if not exists_path(rep):
        #Create replica folder if not exists
        create_dir(rep)
        logger.info(f"Created \"{rep}\"")
        print(f"Created \"{rep}\"")

    elif not is_dir(rep):
        raise NotADirectoryError(f"Replica is not a directory: \"{rep}\"")

def sync_files(src,replic,logger):
    """
    Updates/Creates the files/folders from replica if different from source folder
    """
    files = get_files_from_dir(src) #Get all content from source folder

    for src_path in files:
        rep_path = get_relpath(src_path,src,replic)

        #Checks if content is a directory and creates in replica if not exists
        if is_dir(src_path):
            if not exists_path(rep_path):
                create_dir(rep_path)
                logger.info(f"Created \"{rep_path}\"")
                print(f"Created \"{rep_path}\"")
        else:
            try:
                #Compares file content and copies from source to replica if different
                if not exists_path(rep_path) or not compare_files(rep_path,src_path):
                        copy_file(src_path,rep_path)
                        logger.info(f"Updated \"{rep_path}\"")
                        print(f"Updated \"{rep_path}\"")
            except (PermissionError,FileNotFoundError) as e:
                logger.warning(f"Skipped file \"{src_path}\": {e}")
                print(f"Skipped file \"{src_path}\": {e}")

def remove_files(src,replic,logger):
    """
    Removes the files/folders from replica if not in source folder
    """
    files = get_files_from_dir(replic)

    for rep_path in files[::-1]:
        src_path = get_relpath(rep_path,replic,src)

        if not exists_path(src_path):
            try:
                if is_dir(rep_path):
                    remove_dir(rep_path)
                else:
                    remove_file(rep_path)
                logger.info(f"Removed \"{rep_path}\"")
                print(f"Removed \"{rep_path}\"")
            except (PermissionError,FileNotFoundError) as e:
                logger.warning(f"Skipped removing file \"{rep_path}\": {e}")
                print(f"Skipped removing file \"{rep_path}\": {e}")


def sync(src,replic,logger):
    check_folders(src,replic,logger)
    sync_files(src,replic,logger)
    remove_files(src,replic,logger)

