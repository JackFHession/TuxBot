import requests
import json

def send_request(user_input, server_url='http://localhost:8000'):
    headers = {'Content-Type': 'application/json'}
    data = {'UserInput': user_input}
    response = requests.post(server_url, headers=headers, data=json.dumps(data))
    return response.json()

if __name__ == '__main__':
    user_input = input("You: ")
    server_url = 'http://localhost:2041'
    response = send_request(user_input, server_url)
    print("Response from server:", response)
