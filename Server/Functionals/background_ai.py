import sys
from JanexUltimate.janexnlg import *
from JanexUltimate.janexpytorch import *
from JanexUltimate.janexpython import *
from JanexUltimate.janexspacy import *
import json
from Utilities.functions import *

map_location = torch.device('cpu')

settings = loadconfig("./Settings/config.json")

class TaskAI:
    def __init__(self):
        self.classifier = JanexPT("long_term_memory/tasks.json")
        self.classifier.modify_data_path("long_term_memory/taskdata.pth")
        self.previous_input = None
        self.response_check()
        self.classifier.set_device('cpu')

    def compare(self, input_string):
        self.response_check()
        answer = input_string
        self.previous_input = input_string
        intent_class = self.get_class()
        similarity = 0
        highest_similarity = 0
        most_similar_response = None
        if intent_class:
            return intent_class
        else:
            return None

    def get_class(self):
        input_string = self.previous_input
        intent_class = self.classifier.pattern_compare(input_string)
        return intent_class

    def response_check(self):
        self.settings = loadconfig("./Settings/config.json")
        self.response_setting = self.settings.get("response-type")


if __name__ == "__main__":
    main()
