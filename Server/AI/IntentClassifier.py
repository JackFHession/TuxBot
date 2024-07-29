import sys

from JanexUltimate.janexpytorch import *
from JanexUltimate.janexpython import *

class Classifier:
    def __init__(self):
        self.classifier = JanexPT("long_term_memory/intents.json")
        self.classifier.modify_data_path("long_term_memory/data.pth")
    
    def classify(self, input_string):
        intent_class = self.classifier.pattern_compare(input_string)
        self.intent_class = intent_class
        return intent_class

if __name__ == "__main__":
    AI = Classifier()
    UserInput = input("You: ")
    intent_class = AI.classify(UserInput)
    print(intent_class)