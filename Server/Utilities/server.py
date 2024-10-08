from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
import json
import os
from AI.main import *
from AI.inverter import *
import requests

jarvis = JarvisAI()

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')
        post_data = json.loads(post_data)
        message_text = post_data['message']
        sentence = str(message_text)

        with open("short_term_memory/user_input.txt", "w") as file:
            file.write(sentence)

        ResponseOutput = jarvis.say(sentence)
        intent_class = jarvis.get_class()
        accuracy = jarvis.accuracy_from
        print(f"Predicted accuracy: {accuracy}")

        try:
            response= requests.post("https://api.eureka-ai.dev/chat", headers={
                "API-Key": "e9467f38-ab5d-49e2-8c1e-953c548996a1"
                }, data=json.dumps({
                "query": f"{sentence}"
                }))
            responsej = response.json()
            CandidateResponseOutput = responsej.get("response")
            with open("short_term_memory/output.txt", "r") as outfile:
                prev = outfile.read()

            if prev == CandidateResponseOutput:
                ResponseOutput = invert_phrase(sentence)
            else:
                ResponseOutput = CandidateResponseOutput
            
            with open("short_term_memory/output.txt", "w") as outfile:
                outfile.write(ResponseOutput)
            
        except:
            pass
        
        with open("short_term_memory/current_class.json", "w") as outjson:
            json.dump(intent_class, outjson, indent=4)
        
        response_data = {
            'response': ResponseOutput,
            'intent_class': intent_class
        }

        response_json = json.dumps(response_data)
        response_bytes = response_json.encode('utf-8')

        self.send_response(200)
        self.send_header('Content-type', 'application/json')  # Set content type to JSON
        self.send_header('Content-length', len(response_bytes))
        self.end_headers()

        self.wfile.write(response_bytes)

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('8000')
    httpd.serve_forever()
