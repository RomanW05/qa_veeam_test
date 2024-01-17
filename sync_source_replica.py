import colorlog
import hashlib
import logging
import os
from json_formatter import formatter
from os import walk
from os.path import exists, join, relpath
import sys



source_folder_path = "C:/Users/yop/Desktop/w/assingments/Veeam/veeam_qa/source"
replica_folder_path = "C:/Users/yop/Desktop/w/assingments/Veeam/veeam_qa/replica"
logging_file_path = "C:/Users/yop/Desktop/w/assingments/Veeam/veeam_qa/logging.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Color handler to console
stdout = colorlog.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
fmt = colorlog.ColoredFormatter(
    "%(name)s: %(white)s%(asctime)s%(reset)s | %(log_color)s%(levelname)s%(reset)s | %(blue)s%(filename)s:%(lineno)s%(reset)s | %(process)d >>> %(log_color)s%(message)s%(reset)s"
)
stdout.setFormatter(fmt)
logger.addHandler(stdout)

# Json handler to file
logHandler = logging.FileHandler(logging_file_path)
logHandler.setFormatter(formatter)
logHandler.setLevel(logging.WARNING)
logger.addHandler(logHandler)


def checksum_file(file_path):
    with open(file_path, 'rb') as file_to_check:
        data = file_to_check.read()
        md5_returned = hashlib.md5(data).hexdigest()
    return md5_returned


def create_file(source_file_path, replica_file_path, buffer_size=1024):
    try:
        with open(source_file_path, 'rb') as source_file:
            with open(replica_file_path, 'wb') as replica_file:
                logger.debug(f'File created: {replica_file_path}')
                while True:
                    buffer_data = source_file.read(buffer_size)
                    if not buffer_data:
                        logger.debug(f'File copied: {source_file_path}')
                        break
                    replica_file.write(buffer_data)
    except FileNotFoundError:
        logger.error(f"File not found: {source_file_path}")
        raise FileNotFoundError
    except PermissionError:
        logger.error(f"Permission denied: {source_file_path} or {replica_file_path}")
        raise PermissionError
    except OSError as e:
        if e.errno == 28:
            logger.error(f'Not enough disk memory to copy files: {e}')
            raise OSError(f'Not enough disk memory to copy files: {e}')
        else:
            logger.error(f"OS error occurred: {e}")
            raise OSError(f"OS error occurred: {e}")


def create_folder(folder_path):
    try:
        os.mkdir(folder_path)
        logger.debug(f'Folder created: {folder_path}')
    except OSError as e:
        if e.errno == 17:
            logger.warning('Trying to create an existing folder')
        else:
            logger.error(f"OS error occurred: {e}")
            raise OSError(f"OS error occurred: {e}")


def remove_file(file_path):
    try:
        os.remove(file_path)
        logger.debug(f'File removed {file_path}')
    except OSError as e:
        logger.error(f'Error while deleting file {file_path}: {e}')


def remove_folder(folder_path):
    try:
        os.rmdir(folder_path)
        logger.debug(f'Folder deleted: {folder_path}')
    except OSError as e:
        if e.errno == 41:
            logger.error(f'Cannot delete a non empty folder: {e}')
        else:
            logger.error(f'Error while deleting folder {folder_path}: {e}')


def operational_tree(source_folder_path, replica_folder_path, topdown=True):
    """
    Creates two dictionaries which contains a filepath as key and a boolean as value. The
    boolean flag represents wheather or not the file is present in the replica folder.
    When copying files to replica topdown=True, when deleting from replica topdown=False 
    """
    files_dictionary = {}
    folder_dictionary = {}
    for dirpath, dirnames, filenames in walk(source_folder_path, topdown=topdown):
        relative_path = relpath(dirpath, source_folder_path)
        for dirname in dirnames:
            relative_path_to_folder = join(relative_path, dirname)
            if exists(join(replica_folder_path, relative_path_to_folder)):
                folder_dictionary[relative_path_to_folder] = True
            else:
                folder_dictionary[relative_path_to_folder] = False

        for filename in filenames:
            relative_path_to_file = join(relative_path, filename)
            if exists(join(replica_folder_path, relative_path_to_file)):
                files_dictionary[relative_path_to_file] = True
            else:
                files_dictionary[relative_path_to_file] = False
    
    return folder_dictionary, files_dictionary


def copy_all_files_from_source(source_folder_path, replica_folder_path, folders_to_create, files_to_create):
    for elem in folders_to_create.items():
        replica_folder = join(replica_folder_path, elem[0])
        if not exists(replica_folder):
            create_folder(replica_folder)

    for elem in files_to_create.items():
        source_file = join(source_folder_path, elem[0])
        replica_file = join(replica_folder_path, elem[0])
        if elem[1]:  # File does exist
            source_checksum = checksum_file(source_file)
            replica_cheksum = checksum_file(replica_file)
            if source_checksum != replica_cheksum:  # Files are different
                create_file(source_file, replica_file)
                logger.debug(f'Modified file: {replica_file}')
            else:
                pass  # Ignore, exact copy
        else:  # Files does not exist
            create_file(source_file, replica_file)


def delete_invalid_files_from_replica(replica_folder_path, folders_to_delete, files_to_delete):
    for elem in files_to_delete.items():
        if not elem[1]:
            replica_file = join(replica_folder_path, elem[0])
            remove_file(replica_file)

    for elem in folders_to_delete.items():
        if not elem[1]:
            replica_folder = join(replica_folder_path, elem[0])
            remove_folder(replica_folder)


def main():
    logger.info(f'Syncronization process started')
    if not exists(source_folder_path) or not exists(replica_folder_path):
        logger.critical('Source or replica paths do not exist')
        raise FileNotFoundError('Source or replica paths do not exist')
    
    folders_to_create, files_to_create = operational_tree(source_folder_path, replica_folder_path)
    folders_to_delete, files_to_delete = operational_tree(replica_folder_path, source_folder_path)
    logger.info(f'Dictionaries to create and delete files and folders done')

    copy_all_files_from_source(source_folder_path, replica_folder_path, folders_to_create, files_to_create)
    logger.info(f'Files and folders created done')

    delete_invalid_files_from_replica(replica_folder_path, folders_to_delete, files_to_delete)
    logger.info(f'Files and folders deleted done')
    logger.info(f'Syncronization process finished')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f'Syncronization process did not finished. Replica folder not synchronized. Error:\n{e}')
