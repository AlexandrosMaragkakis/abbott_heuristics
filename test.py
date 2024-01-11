#import nltk
#nltk.download('wordnet')

try:
    from nltk.corpus import wordnet
except:
    import nltk
    nltk.download('wordnet')
    from nltk.corpus import wordnet



def get_possessive_verbs():
    return [wordnet.synset('have.v.01'), wordnet.synset('own.v.01')]

def calculate_similarity(synset1, synset2):
    # Wu-Palmer Similarity is one of the similarity metrics provided by NLTK
    return synset1.path_similarity(synset2)

# Print and compare definitions of possessive verbs
possessive_verbs = get_possessive_verbs()

for synset in wordnet.synsets('possess', pos=wordnet.VERB):
    print(f"{synset} // {synset.definition()}")
    for example in synset.examples():
        print("\t" + example)
    print()

    # Compare similarity with possessive verbs
    for possessive_verb in possessive_verbs:
        similarity = calculate_similarity(synset, possessive_verb)
        print(f"Similarity with {possessive_verb}: {similarity}")
    print()

