import json
import os 

# Construct the absolute path of the shared_data.json folder 
deploy_dir = os.path.dirname(__file__)  # This gives the absolute path of the directory containing utils.py
shared_data_path = os.path.join(deploy_dir, "shared_data.json")  # Joins it with the filename to get the full path


def get_shared_value(key):
    """
    Reads the shared_data.json file and retrieves a specific key's value.
    
    :param key: The key to retrieve from the JSON file.
    :return: The corresponding value from the JSON file.
    """
    try:
        with open(shared_data_path, "r") as f:
            content = json.load(f)
            value = content.get(key)
            if not value:
                raise ValueError(f"Invalid data in shared_data.json. Ensure '{key}' is present.")
            return value
    except json.JSONDecodeError:
        raise ValueError("Error parsing shared_data.json. Ensure it contains valid JSON data.")


def update_shared_value(dictionary):
    try:
        with open(shared_data_path, 'r') as f:
            content = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        content = {}

    # Add new data to the existing content
    content.update(dictionary)

    # Write the updated content back to the JSON file
    with open(shared_data_path, 'w') as f:
        json.dump(content, f, indent=4)

