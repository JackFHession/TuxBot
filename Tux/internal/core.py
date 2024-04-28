from internal.send_request import *
from layout.layout import *
from utils.functions import *
import random

class Intel:
    def __init__(self):
        self.initialized_layout = layout_template()
    
    def default_interface(self):
        self.initialized_layout.set_face("./faces/Default.txt")
        user_input = self.initialized_layout.get_input()
        FullResponse = send_request(url, user_input)
        print(FullResponse)
        IntentClass = FullResponse.get("intent_class")
        print(IntentClass)
        DoFunction(IntentClass)
        ResponseOutput = FullResponse.get("response")
        tts(ResponseOutput)
        print(ResponseOutput)

