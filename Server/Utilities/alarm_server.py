import socket
import json
import threading
import time
from datetime import datetime, timedelta
from Utilities.functions import *
from Functionals.background_ai import *

Instance = TaskAI()

def play_alarm():
    data = check_for_alarm()
    if data.get("type") == "alarm":
        play_notification_sound("./AudioFiles/alarm_clock.mp3")
    elif data.get("type") == "reminder":
        speak(f"Reminder. {data.get('tag')}")

def check_for_alarm():
    alarms = loadconfig("./Settings/reminders.json")

    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%H:%M")
    
    one_hour_later = (datetime.now() + timedelta(hours=1)).time()
    formatted_one_hour_later = one_hour_later.strftime("%H:%M")

    for alarm in alarms["reminders"]:
        alarm_time = alarm.get("time")
        alarm_type = alarm.get("type")

        if alarm_time == formatted_time:
            return alarm
        elif alarm_time == formatted_one_hour_later and alarm_type == "reminder":
            return alarm
    
    return None

def perform_action(task):
    tasktag = task.get("tag")

    if tasktag == "alarm":
        play_alarm()

def background_run_protocols():
    while True:
        task = None

        if check_for_alarm() is not None:
            task = Instance.compare("Time is matching")

        if task is not None:
            perform_action(task)
        
        time.sleep(60)

def run_protocols():
    print("Background protocols loop is now active.")
    threading.Thread(target=background_run_protocols, args=()).start()

def handle_client(client_socket):
    data = client_socket.recv(1024).decode("utf-8")
    if data == "check_for_alarm":
        task = Instance.compare("Time is matching")
        client_socket.send(json.dumps(task).encode("utf-8"))
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 2060))
    server_socket.listen(5)
    print("Server is listening on port 2060.")

    while True:
        client_socket, _ = server_socket.accept()
        handle_client(client_socket)

if __name__ == "__main__":
    run_protocols()
    start_server()
