import hashlib
import os
from os import walk

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