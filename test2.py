from nltk.corpus import wordnet


verbs_to_check = ["possess", "own", "have", "hold", "control", "retain", "occupy", "acquire", "obtain", "keep"]

# Find synsets for the specified verbs
for verb in verbs_to_check:
    synsets = wordnet.synsets(verb, pos=wordnet.VERB)
    print(f"Synsets for '{verb}':")
    for synset in synsets:
        print(f"{synset} // {synset.definition()}")
    print()
