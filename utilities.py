import json
import os
from pathlib import Path
from argparse import ArgumentTypeError


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
    # handle ValueError: not enough values to unpack (expected 2, got 0)

    if len(list1) == 0 or len(list2) == 0:
        return []
    
    common_elements = list(set(list1) & set(list2))
    return common_elements

def validate_file_argument(file_path):
    if not file_path.endswith(".json"):
        raise ArgumentTypeError("Please provide a JSON file.")
    return file_path
