import json

def calc_len(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    length = len(json_data)
    return length
