import argparse
import json
from googletrans import Translator  # 'googletrans==4.0.0-rc1'
import deepl
from settings import deepl_api_auth_key



def check_json_format(data):
    if not isinstance(data, list):
        raise ValueError("JSON file should contain a list of scenarios.")
    for scenario in data:
        if ("id" not in scenario) or (("el_text" not in scenario) and ("en_text" not in scenario)):
            raise ValueError("Each scenario should have 'id' and either 'el_text' or 'en_text' field.")

def translate_to_greek(scenarios):
    translator = Translator()
    for scenario in scenarios:
        if "el_text" not in scenario:
            en_text = scenario["en_text"]
            el_text = translator.translate(en_text, src="en", dest="el").text
            scenario["el_text"] = el_text

def translate_to_english(scenarios, translation_service="google"):
    for scenario in scenarios:
        #if "en_text" not in scenario: # do not translate if already translated
        el_text = scenario["el_text"]
            
        if translation_service == "google":
            en_text = translate_with_google(el_text)
        elif translation_service == "deepl":
            en_text = translate_with_deepl(el_text)
        else:
            raise ValueError("Invalid translation service. Supported values: 'google' or 'deepl'")
            
        scenario["en_text"] = en_text

def translate_with_google(text):
    translator = Translator()
    return translator.translate(text, src="el", dest="en").text

def translate_with_deepl(text):
    auth_key = deepl_api_auth_key
    if not auth_key:
        raise ValueError("Please set the 'deepl_api_auth_key' environment variable.")
    
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text=text, source_lang="EL", target_lang="EN-US")
    return result.text



def main():
    parser = argparse.ArgumentParser(description="Translate Greek scenarios to English or vice versa.")
    parser.add_argument("json_file", help="Path to the JSON file containing scenarios.")
    parser.add_argument("--service", choices=["google", "deepl"], default="google",
                        help="Translation service to use (default: google)")
    args = parser.parse_args()

    with open(args.json_file, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

    try:
        check_json_format(data)
    except ValueError as e:
        print(f"Invalid JSON format: {e}")
        return

    # Check if translation from Greek to English is needed
    #if any("en_text" not in scenario for scenario in data):
    translate_to_english(data, translation_service=args.service)


    # Check if translation from English to Greek is needed
    #if any("el_text" not in scenario for scenario in data):
    #    translate_to_greek(data, translation_service=args.service)

    # Save the updated scenarios with added English translations in the same file
    with open(args.json_file, "w", encoding="utf-8") as output:
        json.dump(data, output, ensure_ascii=False, indent=2)

    print("Translation complete. Updated JSON saved.")

if __name__ == "__main__":
    main()
