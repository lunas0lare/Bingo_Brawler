import os
import requests
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
   

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, indent = 2, ensure_ascii= False)

def html_parser(link) -> str:
    """
    Fetches the raw HTML content from the given URL
    Args:
        link (str): A valid URL pointing to an HTML resource.

    Returns:
        str: The HTML content retrieved from the URL as a string.
    """
    request = requests.get(link).text
    
    return request

def content_to_file(dir_name, data, file_name):
    """
    Creates a directory (if it does not exist) and writes content to a file.
    Args:
        dir_name (str): Name or path of the directory to create or use.
        data (str): Content to write into the file.
        file_name (str): Name of the file to create inside the directory.
    Return:
        None
    """
    create_project_dir(dir_name)
    write_file(dir_name + '/' + file_name, data)