import argparse
from utilities import load_scenarios_from_file, compare_lists

verb_types_field_names = {"action_verbs": "Functionalities", 
                          "possession_verbs": "Inheritances",
                          "categorization_verbs": "Aggregations", 
                          "modal_verbs": "Restrictions"}

parser = argparse.ArgumentParser(description="Evaluate json fields. You need to run main.py first.") 
parser.add_argument("--file", help="Path to the JSON file containing scenarios.", required=True)
args = parser.parse_args()

scenarios = load_scenarios_from_file(args.file)

for scenario in scenarios:  
    if not scenario.get("useful_action_verbs") or not scenario.get("action_verbs"):
        raise ValueError("Missing 'useful_action_verbs' or 'action_verbs' field in scenario. Make sure you ran main.py first.")
    
    common_nouns = compare_lists(scenario["nouns"], scenario["useful_nouns"])
    common_proper_nouns = compare_lists(scenario["proper_nouns"], scenario["useful_proper_nouns"])
    common_adjectives = compare_lists(scenario["adjectives"], scenario["useful_adjectives"])

    # open txt file to log the results
    with open('results.txt', 'a') as file:
        file.write("\n--------------------------------------------------------------------\n")
        file.write(f"Scenario: {scenario['id']}\n\n")
        file.write(f"Classes: {common_nouns}\n")
        file.write(f"CLass Instances: {common_proper_nouns}\n")
        file.write(f"Attributes: {common_adjectives}\n")

    
    for verb_type_field_name in verb_types_field_names:


        verb_list1 = scenario[verb_type_field_name]
        verb_list2 = scenario[f"useful_{verb_type_field_name}"]

        if not verb_list2:
            continue

        
        common_verbs = compare_lists(verb_list1, verb_list2)
        
        with open('results.txt', 'a') as file:
            file.write(f"{verb_types_field_names[verb_type_field_name]}: {common_verbs}\n")

        #print()
    