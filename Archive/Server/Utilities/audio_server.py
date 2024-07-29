from flask import Flask, request, jsonify
import os
from Utilities.functions import *
from Utilities.transcribe import *

config = loadconfig("./Settings/config.json")

WhisperAI = speech()
WhisperAI.filename = (os.path.join('short_term_memory', 'received.wav'))

port = config.get("default-port")

flaskapp = Flask(__name__)

@flaskapp.route('/', methods=['POST'])
def receive_wav():
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        file.save(os.path.join('short_term_memory', 'received.wav'))
        Transcription = WhisperAI.transcribe()
        os.system(f'./Utilities/send_request http://localhost:{port} "{Transcription}"')

        with open("./short_term_memory/output.txt", "r") as f:
            ResponseOutput = f.read()
    
        with open("./short_term_memory/current_class.json", "r") as f:
            intent_class = json.load(f)

        # Combine ResponseOutput and intent_class into a dictionary
        response_data = {
            "ResponseOutput": ResponseOutput,
            "intent_class": intent_class
        }

        # Return the dictionary as a JSON response
        return response_data

if __name__ == '__main__':
    flaskapp.run(port=config.get("voip-port"))
