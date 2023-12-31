import argparse
import spacy
from utilities import load_scenarios_from_file
import json

#TODO: write function for json file saving

# make argument parser for model choice
parser = argparse.ArgumentParser(description="Use abbott's heuristics in software engineering scenarios using spacy models.") 
parser.add_argument("--model", choices=["sm", "md", "lg", "trf"], help="Choose model to use.", required=True)
args = parser.parse_args()

# Load spacy model
if args.model == "sm":
    nlp_en = spacy.load("en_core_web_sm") # size 12 MB
elif args.model == "md":
    nlp_en = spacy.load("en_core_web_md") # size 40 MB 
elif args.model == "lg":
    nlp_en = spacy.load("en_core_web_lg") # size 560 MB
elif args.model == "trf":
    nlp_en = spacy.load("en_core_web_trf") # size 440 MB, 3 GB with dependencies
else: # cant happen because of "required=True" in parser?
    raise ValueError("Invalid model. Supported values: 'sm', 'md', 'lg', 'trf'")



# Load scenarios from JSON file
scenarios = load_scenarios_from_file('data/scenarios.json')

for scenario in scenarios:
    id = scenario.get("id")
    
    en_text = scenario.get("en_text")  
    if en_text:
        #print("Scenario ID:", id)
        doc = nlp_en(en_text)
        proper_nouns = set()
        nouns = set()
        #rimata_energeias = {}
        #rimata_dilotika_eidous = {}
        #rimata_dilotika_ktisis = {}
        #tropiko_rima = {}
        adjectives = set()
        for token in doc:
            if token.pos_ == "PROPN":
                proper_nouns.add(token.text)
            if token.pos_ == "NOUN":
                nouns.add(token.text)
            if token.pos_ == "ADJ":
                adjectives.add(token.text)
        
        # print("Proper nouns:", proper_nouns)
        # print("Nouns:", nouns)
        # print("Adjectives:", adjectives)
        #print("Model:", model)
        #for ent in doc.ents:
        #    print(ent.text, ent.start_char, ent.end_char, ent.label_, spacy.explain(ent.label_))
        
        #print("\n\n")
                
        # add the sets to the scenario json file
        scenario["proper_nouns_" + args.model] = list(proper_nouns)
        scenario["nouns_" + args.model] = list(nouns)
        scenario["adjectives_" + args.model] = list(adjectives)

# save the updated scenarios to the JSON file
with open('data/scenarios.json', 'w') as f:
    json.dump(scenarios, f, ensure_ascii=False, indent=2)
