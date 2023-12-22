import spacy
#from spacy.lang.el.examples import sentences 

# function to load scenarios from a file
def load_scenario_from_file(file_path):
    with open(file_path, 'r') as file:
        scenario = file.readlines()
        scenario = ' '.join(scenario)
    return scenario

nlp = spacy.load("el_core_news_sm")
#doc = nlp(sentences[0])
scenario = load_scenario_from_file('data/scenario1.txt')
doc = nlp(scenario)
for token in doc:
    if token.pos_ == 'PROPN':
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)