import json
import re

with open('./long_term_memory/Dict.json', 'r') as file:
    config = json.load(file)

patterns = config.get("patterns", {})
default_response = config.get("default_response", "I don't understand that question.")

def invert_phrase(input_phrase):
    input_phrase = re.sub(r'[?!]', '.', input_phrase)
    original_phrase = input_phrase
    for pattern, replacement in patterns.items():
        pattern_regex = re.compile(re.escape(pattern), re.IGNORECASE)
        input_phrase = pattern_regex.sub(replacement, input_phrase)
    if input_phrase == original_phrase:
        return default_response
    return input_phrase

if __name__ == "__main__":
    Userinput = input("You: ")
    ResponseOutput = invert_phrase(Userinput)
    print(f"Bot: {ResponseOutput}")
