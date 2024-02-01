 # Abbott's Heuristics in Software Engineering Scenarios

 This project aims to apply Abbott's heuristics to identify classes, class instances, attributes, and functionalities from software engineering scenarios written in natural language. The project uses spacy, nltk, wordnet, transformers, googletrans, and deepl libraries to perform natural language processing and translation tasks.

 ## Installation

 Initialize and activate a virtual environment:
 ```bash
 python3 -m venv venv
 source venv/bin/activate
 ```

 To install the required libraries, run the following command:

 ```bash
 pip install -r requirements.txt
 ```


 You also need to set the `deepl_api_auth_key` environment variable with your DeepL API key, if you want to use the DeepL translation service.

 ## Usage

 The main script of the project is `main.py`, which takes four arguments:

 - `-m`: The spacy model to use for token classification. Best results with 'trf' and 'lg'.
 - `-i`: The path to the JSON file containing scenarios.
 - `-o`: The path to the output JSON file.
 - `-v`: The method for verb classification. Either 'wordnet' or 't5'.

 For example, to run the script with the 'trf' model, the 'scenarios.json' file as input, the 'output.json' file as output, and the 't5' method for verb classification, run the following command:

 ```bash
 python main.py -m trf -i scenarios.json -o output.json -v t5
 ```

 The input JSON file should contain a list of scenarios, each with an 'id' and either an 'el_text' or an 'en_text' field. For example:

 ```json
 [
   {
     "id": "1",
     "el_text": "Ένας χρήστης μπορεί να δημιουργήσει ένα λογαριασμό στο Facebook με ένα όνομα, ένα email και έναν κωδικό πρόσβασης."
   },
   {
     "id": "2",
     "en_text": "A user can create a Facebook account with a name, an email, and a password."
   }
 ]
 ```

 The output JSON file will contain the same scenarios, with additional fields for the extracted words according to Abbott's heuristics. For example:

 ```json
 [
   {
     "id": "1",
     "el_text": "Ένας χρήστης μπορεί να δημιουργήσει ένα λογαριασμό στο Facebook με ένα όνομα, ένα email και έναν κωδικό πρόσβασης.",
     "en_text": "A user can create a Facebook account with a name, an email, and a password.",
     "proper_nouns": [
       "Facebook"
     ],
     "nouns": [
       "user",
       "account",
       "name",
       "email",
       "password"
     ],
     "adjectives": [],
     "modal_verbs": [
       "can"
     ],
     "possession_verbs": [],
     "categorization_verbs": [],
     "action_verbs": [
       "create"
     ]
   },
   {
     "id": "2",
     "en_text": "A user can create a Facebook account with a name, an email, and a password.",
     "proper_nouns": [
       "Facebook"
     ],
     "nouns": [
       "user",
       "account",
       "name",
       "email",
       "password"
     ],
     "adjectives": [],
     "modal_verbs": [
       "can"
     ],
     "possession_verbs": [],
     "categorization_verbs": [],
     "action_verbs": [
       "create"
     ]
   }
 ]
 ```

 The project also includes some utility scripts, such as:

 - `translate.py`: A script to translate Greek scenarios to English or vice versa, using either Google or DeepL translation service.
 - `evaluate_json.py`: A script to evaluate the JSON fields according to Abbott's heuristics, and save the results in a text file.

 For more details on how to use these scripts, please refer to their source code and comments.

 ## License

 This project is licensed under the MIT License - see the LICENSE file for details.
