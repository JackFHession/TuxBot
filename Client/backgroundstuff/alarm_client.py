import requests
import json
import threading
from Utilities.functions import *

def send_request(request):
    config = loadconfig("./Settings/config.json")
    url = config.get("ThirdIP")

    response = requests.post(url, data=request.encode("utf-8"))
    return json.loads(response.text)

def send_request_in_background():
    while True:
        request = "check_for_alarm"
        task = send_request(request)
        print(task)
        # Adjust sleep duration as needed
        time.sleep(60)

if __name__ == "__main__":
    # Start the background thread
    threading.Thread(target=send_request_in_background).start()
