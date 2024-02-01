from nltk.corpus import wordnet as wn
import nltk
from nltk.wsd import lesk

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

def load_synsets_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            synsets = [synset.strip() for synset in file.readlines()]
        return synsets
    except FileNotFoundError:
        print("File not found.")
        return None


def disambiguate_and_check(sentence, word, word_list):
    verb_synset = lesk(sentence, word, 'v')
    if word == 'is':
        print(str(verb_synset))
    return str(verb_synset) in word_list

def find_possessive_and_stative_synsets():

    # create an empty list to store the verb synsets that show possession
    possession_verbs = []

    # create an empty list to store the verb synsets that show categorization
    categorization_verbs = []

    # iterate over all the verbs synsets in wordnet
    for synset in wn.all_synsets(pos=wn.VERB):

        # check if the synset has the lexname attribute equal to 'verb.possession'
        if synset.lexname() == 'verb.possession':
            possession_verbs.append(synset)

        # check if the synset has the lexname attribute equal to 'verb.categorization'
        if synset.lexname() == 'verb.stative':
            categorization_verbs.append(synset)

    # Save possession_verbs to a text file
    with open('possession_verbs_synsets.txt', 'w') as f:
        for synset in possession_verbs:
            f.write(str(synset) + '\n')

    # Save categorization_verbs to a text file
    with open('categorization_verbs_synsets.txt', 'w') as f:
        for synset in categorization_verbs:
            f.write(str(synset) + '\n')

