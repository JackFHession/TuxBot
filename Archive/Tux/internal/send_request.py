import requests
import json

with open("./Settings/configuration.json", "r") as config:
    data = json.load(config)
    url = data.get("dest")

def send_request(url, text):
    headers = {'Content-Type': 'application/json'}
    payload = {'message': text}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return e

if __name__ == "__main__":
    response = send_request(url, "Hello")
    print(response.text)
