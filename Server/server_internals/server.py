from AI.Inverter import *
from AI.ThirdParty import *
from AI.IntentClassifier import *

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

AI = Classifier()
Responder = Inverter()
Eureka = Eureka_Connect()

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        UserInput = data['UserInput']
        
        intent_class = AI.classify(UserInput)
        try:
            ResponseOutput = Eureka.send_request(UserInput)
        except:
            ResponseOutput = Responder.invert_phrase(UserInput)
            if ResponseOutput == "Null.":
                ResponseOutput = random.choice(intent_class["responses"])
        
        ResponseJSON = {"response": ResponseOutput, "intent_class": intent_class}
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(ResponseJSON).encode('utf-8'))

def start_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

def stop_server(httpd):
    print('Stopping server...')
    httpd.server_close()

if __name__ == '__main__':
    server = start_server(8000)
