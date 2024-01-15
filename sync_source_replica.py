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