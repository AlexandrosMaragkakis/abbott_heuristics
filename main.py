import argparse
import spacy
from utilities import load_scenarios_from_file
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Text2TextGenerationPipeline

d1 = "have ownership or possession of"
d2 = "is of type"
d3 = "perform an action"

verb_types = [d1, d2, d3]
modal_verbs_list = ["can", "could", "might", "must", "shall", "should", "will", "would", "must", "may"]


# olo mazi peripou 10gb ram se ubuntu
# model size = 3.95 GB
pipe = Text2TextGenerationPipeline(model=AutoModelForSeq2SeqLM.from_pretrained("jpwahle/t5-large-word-sense-disambiguation"),
                                   tokenizer=AutoTokenizer.from_pretrained("jpwahle/t5-large-word-sense-disambiguation"))


def wsd_gen(word, context, d1, d2, d3):
    question = 'question: question: which description " ' + d1 + ' " , " ' + d2 + ' " , or " ' + d3 + ' " describes the word' + ' " ' + word + ' " '
    descriptions_context = 'best in the following context? context: ' + context + "'"
    raw_input = question + descriptions_context
    output = pipe(raw_input)[0]['generated_text']
    return output

# make argument parser for model choice
parser = argparse.ArgumentParser(description="Use abbott's heuristics in software engineering scenarios using spacy models.") 
parser.add_argument("--model", choices=["sm", "md", "lg", "trf"], help="Choose model to use. Best results with 'trf'.", required=True)
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

# save the updated scenarios to the JSON file
with open('data/scenarios.json', 'w') as f:
    json.dump(scenarios, f, ensure_ascii=False, indent=2)
