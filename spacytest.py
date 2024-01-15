import spacy
from utilities import load_scenarios_from_file
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Text2TextGenerationPipeline

# olo mazi peripou 10gb ram se ubuntu
# model size = 3.95 GB
pipe = Text2TextGenerationPipeline(model=AutoModelForSeq2SeqLM.from_pretrained("jpwahle/t5-large-word-sense-disambiguation"),
                                   tokenizer=AutoTokenizer.from_pretrained("jpwahle/t5-large-word-sense-disambiguation"))

def wsd_gen(word, context, d1, d2, d3):
    question = 'question: which description from " ' + d1 + ' " , " ' + d2 + ' " , or " ' + d3 + ' " describes the word' + ' " ' + word + ' " '
    descriptions_context = 'best in the following context? context: ' + context + "'"
    raw_input = question + descriptions_context
    output = pipe(raw_input)[0]['generated_text']
    return output

d1 = "have ownership or possession of"
d2 = "is of type"
d3 = "perform an action"

verb_types = [d1, d2, d3]


scenarios = load_scenarios_from_file('data/scenarios.json')

nlp = spacy.load("en_core_web_trf")



wrong_guesses = 0
counter = 0

for scenario in scenarios:
    en_text = scenario.get("en_text")  

    doc = nlp(en_text)

    # Iterate through each token in the processed document
    for token in doc:
        # Check if the token is a verb
        if token.pos_ == "VERB":
            counter += 1
            # Print the sentence and the position of the verb within the sentence
            sentence = list(token.sent)
            verb_position = sentence.index(token)
            
            
            # Remove all single and double quotes from the sentence
            
            sentence_text = [t.text.replace("'", "").replace('"', '') for t in sentence] 

            # Add single quotes around the verb
            sentence_text[verb_position] = f"' {sentence_text[verb_position]} '"
            # Reduce the sentence to contain n words before and after the verb
            #sentence_text = sentence_text[max(0, verb_position - 10):min(verb_position + 10, len(sentence_text))]
            

            
            formatted_sentence = " ".join(sentence_text)
            print(formatted_sentence)
            print(f"Verb: {token.text}, Position: {verb_position}")
            verb_type =wsd_gen(word=token.text, context=formatted_sentence, d1=d1, d2=d2, d3=d3)
            print(verb_type)
            print()
            if verb_type not in verb_types:
                wrong_guesses += 1

print(f"\nWrong guesses: {wrong_guesses}")
print(f"Total verbs: {counter}")

