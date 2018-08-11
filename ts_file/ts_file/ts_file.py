import json
import os

def save_json(data, json_filename):
    os.makedirs(os.path.dirname(json_filename), exist_ok=True)
    with open(json_filename, 'w') as f:
        json.dump(data, f)

def get_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def delete(filename):
    os.remove(filename)
