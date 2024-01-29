import argparse
from utilities import load_scenarios_from_file, compare_lists

verb_types_field_names = ["action_verbs", "possession_verbs", "categorization_verbs", "modal_verbs"]

parser = argparse.ArgumentParser(description="Evaluate json fields. You need to run main.py first.") 
parser.add_argument("--file", help="Path to the JSON file containing scenarios.", required=True)
args = parser.parse_args()

scenarios = load_scenarios_from_file(args.file)

for scenario in scenarios:  
    if not scenario.get("useful_action_verbs") or not scenario.get("action_verbs"):
        raise ValueError("Missing 'useful_action_verbs' or 'action_verbs' field in scenario. Make sure you ran main.py first.")
    print("Scenario ID:", scenario["id"])
    print("------------")
    for verb_type_field_name in verb_types_field_names:


        verb_list1 = scenario[verb_type_field_name]
        verb_list2 = scenario[f"useful_{verb_type_field_name}"]

        if not verb_list2:
            continue

        
        common_verbs, uncommon_verbs = compare_lists(verb_list1, verb_list2)
        
        print(f"Correctly identified {verb_type_field_name}: {common_verbs}")
        print(f"Incorrectly identified {verb_type_field_name} verbs: ", uncommon_verbs)
        
        print()
    