import json


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

# return the common elements
def compare_lists(list1, list2):
    # handle ValueError: not enough values to unpack (expected 2, got 0)

    if len(list1) == 0 or len(list2) == 0:
        return []
    
    common_elements = list(set(list1) & set(list2))
    return common_elements
