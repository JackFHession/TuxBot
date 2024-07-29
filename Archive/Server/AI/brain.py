import sys
from JanexUltimate.janexnlg import *
from JanexUltimate.janexpytorch import *
from JanexUltimate.janexpython import *
from JanexUltimate.janexspacy import *
import json
from Utilities.functions import *

map_location = torch.device('cpu')

settings = loadconfig("./Settings/config.json")

class SimpleBrain:
    def __init__(self):
        self.classifier = JanexPT("long_term_memory/intents.json")
        self.classifier.modify_data_path("long_term_memory/data.pth")
        self.previous_input = None
        self.response_check()
        self.defaultnlgsize = "en_core_web_sm"
        self.NLG = NLG(self.defaultnlgsize, "./long_term_memory/janex.bin")
        self.classifier.set_device('cpu')

    def receive_input(self, input_sentence):
        self.input_sentence = input_sentence

    def process_input(self):
        if self.response_setting == "random":
            self.NLG = NLG(self.defaultnlgsize, "./long_term_memory/janex.bin")
        self.response_check()
        answer = self.input_sentence
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
        
        self.transform()
        return intent_class
    
    def transform(self):
        # Transform self.input_sentence into a self.output_sentence

    def output_result(self, processed_sentence):
        # Placeholder for outputting result
        print("Output:", processed_sentence)

# Example usage
if __name__ == "__main__":
    brain = SimpleBrain()

    # Receive input
    input_sentence = "Hello Bob, I'm Dave. How are you?"
    brain.receive_input(input_sentence)

    # Process input
    processed_sentence = brain.process_input()

    # Output result
    brain.output_result(processed_sentence)
