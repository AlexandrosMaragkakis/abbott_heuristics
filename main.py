import argparse
parser = argparse.ArgumentParser(description="Use abbott's heuristics in software engineering scenarios using spacy models.") 
parser.add_argument("--model", choices=["sm", "md", "lg", "trf"], help="Choose model to use. Best results with 'trf'.", required=True)
parser.add_argument("--file", help="Path to the JSON file containing scenarios.", required=True)
args = parser.parse_args()

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

import spacy
print("Loading WSD model... ", end="")
from utilities import load_scenarios_from_file, wsd_gen
print("Done.")
import json

d1 = "have ownership or possession of"
d2 = "is of type"
d3 = "perform an action"

verb_types = [d1, d2, d3]
modal_verbs_list = ["can", "could", "might", "must", "shall", "should", "will", "would", "must", "may"]



print("Loading spacy model...", end="")
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
print("Done.")


# Load scenarios from JSON file
scenarios = load_scenarios_from_file(args.file)
counter = 1

for scenario in scenarios:
    
    print(f"Processing scenario {counter}/{len(scenarios)}")

    try: 
        en_text = scenario.get("en_text")
    except KeyError:
        raise ValueError("Missing 'en_text' field in scenario. Make sure you ran translate.py first.")
    
    doc = nlp_en(en_text)
    proper_nouns = set()
    nouns = set()
    adjectives = set()
    modal_verbs = set()
    possession_verbs = set()
    categorization_verbs = set()
    action_verbs = set()
    for token in doc:
        if token.pos_ == "PROPN":
            proper_nouns.add(token.text)
        elif token.pos_ == "NOUN":
            nouns.add(token.text)
        elif token.pos_ == "ADJ":
            adjectives.add(token.text)
        elif token.lemma_.lower() in modal_verbs_list:
            modal_verbs.add(token.text)
        elif token.pos_ == "VERB":
            sentence = list(token.sent)
            verb_position = sentence.index(token)
                
            # remove all single and double quotes from the sentence
            sentence_text = [t.text.replace("'", "").replace('"', '') for t in sentence]

            # add single quotes around the verb
            sentence_text[verb_position] = f"' {sentence_text[verb_position]} '"

            formatted_sentence = " ".join(sentence_text)
            verb_type = wsd_gen(word=token.text, context=formatted_sentence, d1=d1, d2=d2, d3=d3)
            if verb_type in verb_types:
                if verb_type == d1:
                    possession_verbs.add(token.text)
                elif verb_type == d2:
                    categorization_verbs.add(token.text)
                elif verb_type == d3:
                    action_verbs.add(token.text)
                   
        # add the sets to the scenario json file
        scenario["proper_nouns_" + args.model] = list(proper_nouns)
        scenario["nouns_" + args.model] = list(nouns)
        scenario["adjectives_" + args.model] = list(adjectives)
        scenario["modal_verbs"] = list(modal_verbs)
        scenario["possession_verbs"] = list(possession_verbs)
        scenario["categorization_verbs"] = list(categorization_verbs)
        scenario["action_verbs"] = list(action_verbs)

    counter += 1

# save the updated scenarios to a new JSON file
with open('output.json', 'w') as f:
    json.dump(scenarios, f, ensure_ascii=False, indent=2)
    print("Successfully saved updated scenarios to output.json")
