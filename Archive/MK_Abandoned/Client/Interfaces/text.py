from Utilities.send_request import *

def text_interface():
    while True:
        message = input("You: ")
        response = send_request(message, SIP)
        return response

