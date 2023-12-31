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


