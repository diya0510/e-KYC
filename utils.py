import yaml
import os
import json
import time

def file_exists(file_path):
    is_exist=os.path.exists(file_path)
    if is_exist:
        return True

def read_yaml(path_to_yaml: str) -> dict:
    if not os.path.exists(path_to_yaml):
        print(f"[ERROR] YAML file not found: {path_to_yaml}")
        return {}

    with open(path_to_yaml, 'r') as yaml_file:
        try:
            content = yaml.safe_load(yaml_file)
            if content is None:
                print(f"[WARNING] YAML file '{path_to_yaml}' is empty.")
                return {}
            return content
        except yaml.YAMLError as e:
            print(f"[ERROR] Failed to parse YAML file: {e}")
            return {}



def create_dirs(dirs: list):
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)

