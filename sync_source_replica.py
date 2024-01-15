import hashlib
import os
from os import walk
from os.path import exists, join, relpath

source_folder_path = "C:/Users/yop/Desktop/w/assingments/Veeam/veeam_qa/source"
replica_folder_path = "C:/Users/yop/Desktop/w/assingments/Veeam/veeam_qa/replica"
logging_file_path = "C:/Users/yop/Desktop/w/assingments/Veeam/veeam_qa/logging.log"

def checksum_file(file_name):
    with open(file_name, 'rb') as file_to_check:
        data = file_to_check.read()
        md5_returned = hashlib.md5(data).hexdigest()
    return md5_returned

def create_file(source_file_path, replica_file_path, buffer_size=1024):
    with open(source_file_path, 'rb') as source_file:
        with open(replica_file_path, 'wb') as replica_file:
            while True:
                buffer_data = source_file.read(buffer_size)
                if not buffer_data:
                    break
                replica_file.write(buffer_data)

def create_folder(folder_path):
    os.mkdir(folder_path)

def remove_file(file_path):
    os.remove(file_path)

def remove_folder(folder_path):
    os.rmdir(folder_path)


def operational_tree(source_folder_path, replica_folder_path, topdown=True):
    """
    Creates two dictionaries which contains a filepath as key and a boolean as value. The
    flag represents wheather or not the file is present in the replica folder.
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
            print(f'Created: {replica_folder}')

    for elem in files_to_create.items():
        source_file = join(source_folder_path, elem[0])
        replica_file = join(replica_folder_path, elem[0])
        if elem[1]:  # File does exist
            source_checksum = checksum_file(source_file)
            replica_cheksum = checksum_file(replica_file)
            if source_checksum != replica_cheksum:  # Files are different
                # Copying file log
                create_file(source_file, replica_file)
                print(f'Modified: {source_file}')
            else:
                pass  # Ignore exact copy
        else:  # Files does not exist
            # Create file log
            create_file(source_file, replica_file)
            print(f'Created: {source_file}')


def delete_invalid_files_from_replica(replica_folder_path, folders_to_delete, files_to_delete):
    for elem in files_to_delete.items():
        if not elem[1]:
            replica_file = join(replica_folder_path, elem[0])
            remove_file(replica_file)
            print(f'Deleted: {replica_file}')

    for elem in folders_to_delete.items():
        if not elem[1]:
            replica_folder = join(replica_folder_path, elem[0])
            remove_folder(replica_folder)
            print(f'Deleted: {replica_folder}')

def main():
    folders_to_create, files_to_create = operational_tree(source_folder_path, replica_folder_path)
    folders_to_delete, files_to_delete = operational_tree(replica_folder_path, source_folder_path, False)

    copy_all_files_from_source(source_folder_path, replica_folder_path, folders_to_create, files_to_create)
    delete_invalid_files_from_replica(replica_folder_path, folders_to_delete, files_to_delete)

if __name__ == "__main__":
    main()