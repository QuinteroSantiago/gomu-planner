import json

def load_data(file_path):
    """ Load data from a JSON file. """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return an empty dict if no file exists

def save_data(file_path, data):
    """ Save data to a JSON file. """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
