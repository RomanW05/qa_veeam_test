import hashlib
import os
from os import walk
from os.path import exists, join, relpath

source_folder_path = "C:/Users/yop/Desktop/w/assingments/Veeam/source"
replica_folder_path = "C:/Users/yop/Desktop/w/assingments/Veeam/replica"
logging_file_path = "C:/Users/yop/Desktop/w/assingments/Veeam/logging.log"

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