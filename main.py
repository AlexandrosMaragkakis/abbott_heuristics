import warnings
import spacy
from spacy.cli import download
from utilities import load_scenarios_from_file, validate_file_argument, save_scenarios_to_file, validate_json
import argparse

parser = argparse.ArgumentParser(description="Use abbott's heuristics in software engineering scenarios.") 
parser.add_argument("-m", choices=["sm", "md", "lg", "trf"], help="Choose spacy model to use for token classification. Best results with 'trf'.", required=True)
parser.add_argument("-i", metavar="input_file", help="Path to the JSON file containing scenarios.", required=True, type=validate_file_argument)
parser.add_argument("-o", metavar="output_file", help="Path to the output JSON file.", required=True, type=validate_file_argument)
parser.add_argument("-v", choices=["wordnet", "t5"], help="Choose method for verb classification.", required=True)
args = parser.parse_args()

validate_json(args.i)

if args.v == "t5":
    print("Model size = 3.95 GB")
    print("Free RAM required to run model = 5 GB")
    # ask if user wants to continue
    confirm = input("Do you want to continue? (y/n) ")
    if confirm.lower() != "y":
        exit()
    warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
    print("Loading WSD model... ", end="")
    from model_utilities import wsd_gen
    print("Done")

elif args.v == "wordnet":
    from verb_classification_wordnet import disambiguate_and_check, load_synsets_from_file
    print("Loading verb synsets... ", end="")
    possession_verbs_synsets = load_synsets_from_file("possession_verbs_synsets.txt")
    categorization_verbs_synsets = load_synsets_from_file("categorization_verbs_synsets.txt")
    print("Done")
else:
    print("Invalid value for -v. Must be 'wordnet' or 't5'.")
    exit()



# descriptions for verb disambiguation
d1 = "have ownership or possession of"
d2 = "is of type"
d3 = "perform an action"

verb_types = [d1, d2, d3]
modal_verbs_list = ["can", "could", "might", "must", "shall", "should", "will", "would", "must", "may"]

print("Loading spacy model...", end="")
if not spacy.util.is_package(f"en_core_web_{args.m}"):
        print(f"Model '{args.m}' not found.")
        
        # ask if user wants to download the model, print model sizes
        print("Model sizes: sm = 12 MB, md = 40 MB, lg = 560 MB, trf = 440 MB")
        confirm = input("Do you want to download the model? (y/n) ")
        if confirm.lower() != "y":
            exit()
        

        download(f"en_core_web_{args.m}")

# Load spacy model
# if args.m == "sm":
#     nlp_en = spacy.load("en_core_web_sm") # size 12 MB
# elif args.m == "md":
#     nlp_en = spacy.load("en_core_web_md") # size 40 MB 
# elif args.m == "lg":
#     nlp_en = spacy.load("en_core_web_lg") # size 560 MB
# elif args.m == "trf":
#     nlp_en = spacy.load("en_core_web_trf") # size 440 MB, 3 GB with dependencies
# else: # cant happen because of "required=True" in parser?
#     raise ValueError("Invalid model. Supported values: 'sm', 'md', 'lg', 'trf'")
print("Done.")

nlp_en = spacy.load(f"en_core_web_{args.m}")

# Load scenarios from input file
scenarios = load_scenarios_from_file(args.i)



for scenario in scenarios:
    print("Processing scenario with ID: " + scenario["id"])

    try: 
        en_text = scenario.get("en_text")
    except KeyError:
        raise ValueError("Missing 'en_text' field in scenario. Make sure you ran translate.py first.")
    
    doc = nlp_en(en_text)

    # initialize sets
    proper_nouns = set()
    nouns = set()
    adjectives = set()
    modal_verbs = set()
    possession_verbs = set()
    categorization_verbs = set()
    action_verbs = set()

    for token in doc:
        # 'is' -> AUX, maybe hard code it?

        # Check if the token is a proper noun
        if token.pos_ == "PROPN":
            proper_nouns.add(token.text)
        # Check if the token is a noun
        elif token.pos_ == "NOUN":
            nouns.add(token.text)
        # Check if the token is an adjective
        elif token.pos_ == "ADJ":
            adjectives.add(token.text)
        # Check if the token is a modal verb
        elif token.lemma_.lower() in modal_verbs_list:
            modal_verbs.add(token.text)
        # Check if the token is a verb    
        elif token.pos_ == "VERB":
            sentence = list(token.sent)

            if args.v == 't5':
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
            else:
                if disambiguate_and_check(token.sent, token.text, possession_verbs_synsets):
                    possession_verbs.add(token.text)
                elif disambiguate_and_check(token.sent, token.text, categorization_verbs_synsets):
                    categorization_verbs.add(token.text)
                else:
                    action_verbs.add(token.text)
            
                   
        # add the sets to the scenario json file
        scenario["proper_nouns"] = list(proper_nouns)
        scenario["nouns"] = list(nouns)
        scenario["adjectives"] = list(adjectives)
        scenario["modal_verbs"] = list(modal_verbs)
        scenario["possession_verbs"] = list(possession_verbs)
        scenario["categorization_verbs"] = list(categorization_verbs)
        scenario["action_verbs"] = list(action_verbs)



save_scenarios_to_file(args.o, scenarios)
