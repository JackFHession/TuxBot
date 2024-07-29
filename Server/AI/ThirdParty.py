import requests
import json

class Eureka_Connect:
    def __init__(self):
        with open("./long_term_memory/Eureka_API.json") as file:
            API_Key = json.load(file)
            self.API_Key = API_Key.get("API_Key")
    
    def send_request(self, message):
        response = requests.post("https://URL/chat", headers={
                "API-Key": f"{self.API_Key}"
                }, data=json.dumps({
                "query": f"{message}"
                }))

        return response

if __name__ == "__main__":
    Eureka = Eureka_Connect()
    Message = input("You: ")
    ResponseOutput = Eureka.send_request(Message)