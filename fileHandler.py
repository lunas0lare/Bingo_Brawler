import os
from dataclasses import asdict
import json
def create_project_dir(directory: str):
    """
    create a new directory if not exists
    """
    if not os.path.exists(directory):
        print(f"creating directory: {directory}")
        os.makedirs(directory)

def write_file(file_name: str, data):
    """
    write data into file
    """
    with open(file_name, 'w') as f:
        f.write(data)
    f.close()

def delete_file_content(file_name: str):
    with open(file_name, 'w') as f:
        pass

def create_file(file_name: str, data):
    if not os.path.isfile(file_name):
        write_file(file_name, data)

def append_to_file(file_name: str, data):
    with open(file_name, 'a') as f:
        f.write(data + '\n')
    f.close()

def read_file(file_name) -> str:
    with open(file_name, 'r') as f:
        return f.read()
    f.close()

def save_to_json(file_name, extracted_data: list):
    """
    convert data to json\n

    extracted_data: a list of objects
    """
   
    player_dicts = [asdict(p) for p in extracted_data]

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(player_dicts, f, indent = 2)