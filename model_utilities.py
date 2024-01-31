from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Text2TextGenerationPipeline


# olo mazi sxedon 10gb ram se ubuntu
# model size = 3.95 GB
pipe = Text2TextGenerationPipeline(model=AutoModelForSeq2SeqLM.from_pretrained("jpwahle/t5-large-word-sense-disambiguation"),
                                   tokenizer=AutoTokenizer.from_pretrained("jpwahle/t5-large-word-sense-disambiguation"))

def wsd_gen(word, context, d1, d2, d3):
    """
    Generate a word sense disambiguation (WSD) for the given word in the context provided.
    
    Args:
        word (str): The word for which WSD is to be generated.
        context (str): The context in which the word is used.
        d1 (str): Description 1 for disambiguation.
        d2 (str): Description 2 for disambiguation.
        d3 (str): Description 3 for disambiguation.
    
    Returns:
        str: The generated text as the output of the WSD process.
    """
    question = 'question: question: which description " ' + d1 + ' " , " ' + d2 + ' " , or " ' + d3 + ' " describes the word' + ' " ' + word + ' " '
    descriptions_context = 'best in the following context? context: ' + context + "'"
    raw_input = question + descriptions_context
    output = pipe(raw_input)[0]['generated_text']
    return output