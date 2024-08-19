import os
import json
from utils.functions import *

def read_json(file):
    with open(file, "r") as json_file:
        data = json.load(json_file)
    
    return data
