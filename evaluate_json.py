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

output_file = "results.txt"

for scenario in scenarios:  
    if not scenario.get("action_verbs"):
        raise ValueError("Missing 'action_verbs' field in scenario. Make sure you ran main.py first.")
    
    try : 
        scenario["useful_action_verbs"]
        common_nouns = compare_lists(scenario["nouns"], scenario["useful_nouns"])
        common_proper_nouns = compare_lists(scenario["proper_nouns"], scenario["useful_proper_nouns"])
        common_adjectives = compare_lists(scenario["adjectives"], scenario["useful_adjectives"])

        # open txt file to log the results
        with open(output_file, 'a') as file:
            file.write("\n--------------------------------------------------------------------\n")
            file.write(f"Scenario: {scenario['id']}\n\n")
            file.write(f"Classes: {common_nouns}\n")
            file.write(f"CLass Instances: {common_proper_nouns}\n")
            file.write(f"Attributes: {common_adjectives}\n")

        
        for verb_type_field_name in verb_types_field_names:


            verb_list1 = scenario[verb_type_field_name]
            verb_list2 = scenario[f"useful_{verb_type_field_name}"]

            if not verb_list2 or not verb_list1:
                continue

            
            common_verbs = compare_lists(verb_list1, verb_list2)
            
            with open(output_file, 'a') as file:
                file.write(f"{verb_types_field_names[verb_type_field_name]}: {common_verbs}\n")
    except KeyError:
        #raise ValueError("Missing 'useful_action_verbs' field in scenario. Make sure you ran main.py first.")
    #if scenario["useful_action_verbs"] and ["useful_modal_verbs"] and ["useful_categorization_verbs"] and ["useful_possession_verbs"]:
        

    
        with open(output_file, 'a') as file:
            file.write("\n--------------------------------------------------------------------\n")
            file.write(f"Scenario: {scenario['id']}\n\n")
            file.write(f"Possible classes: {scenario['nouns']}\n")
            file.write(f"Possible class instances: {scenario['proper_nouns']}\n")
            file.write(f"Possible attributes: {scenario['adjectives']}\n")
            file.write(f"Possible functionalities: {scenario['action_verbs']}\n")
            file.write(f"Possible inheritances: {scenario['possession_verbs']}\n")
            file.write(f"Possible aggregations: {scenario['categorization_verbs']}\n")
            file.write(f"Possible restrictions: {scenario['modal_verbs']}\n")
        