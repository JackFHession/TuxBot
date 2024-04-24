import sys
from JanexUltimate.janexnlg import *
from JanexUltimate.janexpytorch import *
from JanexUltimate.janexpython import *
from JanexUltimate.janexspacy import *
import json
from Utilities.functions import *

map_location = torch.device('cpu')

settings = loadconfig("./Settings/config.json")

class JarvisAI:
    def __init__(self):
        self.classifier = JanexPT("long_term_memory/intents.json")
        self.classifier.modify_data_path("long_term_memory/speech_data.pth")
        self.previous_input = None
        self.response_check()
        self.defaultnlgsize = "en_core_web_sm"
        self.NLG = NLG(self.defaultnlgsize, "./long_term_memory/janex.bin")
        self.classifier.set_device('cpu')

    def say(self, input_string):
        if self.response_setting == "random":
            self.NLG = NLG(self.defaultnlgsize, "./long_term_memory/janex.bin")
        self.response_check()
        answer = input_string
        self.previous_input = input_string
        if self.response_setting == "random":
            intent_class = self.get_class()
            response = self.NLG.generate_sentence(input_string)
            return response
        else:
            intent_class = self.get_class()
            similarity = 0
            highest_similarity = 0
            most_similar_response = None
            if intent_class:
                input_vectors = self.NLG.get_word_vector(input_string)
                for response in intent_class["responses"]:
                    option_vectors = self.NLG.get_word_vector(response)
                    similarity = calculate_cosine_similarity(input_vectors, option_vectors)
                    if similarity > highest_similarity:
                        highest_similarity = similarity
                        most_similar_response = response

                return most_similar_response

    def get_class(self):
        input_string = self.previous_input
        intent_class = self.classifier.pattern_compare(input_string)
        return intent_class

    def response_check(self):
        self.settings = loadconfig("./Settings/config.json")
        self.response_setting = self.settings.get("response-type")

def main():
    jarvis = JarvisAI()
    if len(sys.argv) != 2:
        print("Usage: python3 main.py 'Text to classify'")
        sys.exit(1)
    input_text = sys.argv[1]
    response = jarvis.say(input_text)
    intent_class = jarvis.get_class()
    with open("short_term_memory/current_class.json", "w") as file:
        json.dump(intent_class, file, indent=4)
    with open("short_term_memory/output.txt", "w") as file:
        file.write(response)

if __name__ == "__main__":
    main()
