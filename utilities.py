import json
import os
from pathlib import Path
from argparse import ArgumentTypeError
from jsonschema import validate, ValidationError

GENERIC_JSON_FORMAT_ERROR = "Invalid JSON format: "

def load_scenarios_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            scenarios = json.load(file)
        return scenarios
    except FileNotFoundError:
        print("File not found.")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON format")
        return None
    

def save_scenarios_to_file(file_name, scenarios):
    """
    Saves scenarios to a file, with automatic file name generation if the file already exists.

    """
    file_path, file_extension = os.path.splitext(file_name)
    index = 1
    while Path(file_path + str(index) + file_extension).exists():
        index += 1
    new_file_path = file_path + str(index) + file_extension
    with open(new_file_path, 'w') as f:
        json.dump(scenarios, f, ensure_ascii=False, indent=2)
        print("Successfully saved updated scenarios in " + new_file_path)


# return the common elements
def compare_lists(list1, list2):

    if len(list1) == 0 or len(list2) == 0:
        return []
    
    common_elements = list(set(list1) & set(list2))
    return common_elements

def validate_file_argument(file_path):
    if not file_path.endswith(".json"):
        raise ArgumentTypeError("Please provide a JSON file.")
    # cant put the code below because I call the same function for the output file
    #if not os.path.isfile(file_path):
        #raise ArgumentTypeError("File not found: " + file_path)
    return file_path

def load_schema(file_path):

    try:
        with open(file_path, 'r') as schema_file:
            return json.load(schema_file)
    except FileNotFoundError:
        raise FileNotFoundError("File not found: " + file_path)
    except json.JSONDecodeError:
        raise json.JSONDecodeError(GENERIC_JSON_FORMAT_ERROR + file_path)

def validate_json(file_path):

    schema = load_schema("schema.json")

    try:
        with open(file_path, "r") as file:
            json_data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("File not found: " + file_path)
    except json.JSONDecodeError:
        raise json.JSONDecodeError(GENERIC_JSON_FORMAT_ERROR + file_path)
    

    try:
        validate(instance=json_data, schema=schema)
        return True
    except ValidationError:
        raise ValidationError(GENERIC_JSON_FORMAT_ERROR + file_path)