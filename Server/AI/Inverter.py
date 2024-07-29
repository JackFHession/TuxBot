import json
import re

class Inverter:
    def __init__(self):
        with open('./long_term_memory/invert_dict.json', 'r') as file:
            self.config = json.load(file)

        self.patterns = self.config.get("patterns", {})
        self.default_response = self.config.get("default_response", "I don't understand that question.")

    def invert_phrase(self, input_phrase):
        input_phrase = re.sub(r'[?!]', '.', input_phrase)
        original_phrase = input_phrase
        for pattern, replacement in self.patterns.items():
            pattern_regex = re.compile(re.escape(pattern), re.IGNORECASE)
            input_phrase = pattern_regex.sub(replacement, input_phrase)
        if input_phrase == original_phrase:
            return self.default_response
        return input_phrase

if __name__ == "__main__":
    Invert = Inverter()

    Userinput = input("You: ")
    ResponseOutput = Invert.invert_phrase(Userinput)
    print(f"Bot: {ResponseOutput}")
