from Utilities.send_request import *
from Utilities.functions import *
from Interfaces.voice import *
from Interfaces.text import *

Mode = input("Mode: ")
Mode = Mode.lower()

if Mode == "voice":
    voice_interface()
elif Mode == "text":
    text_interface()
