import json
import os
import sys
import threading
from datetime import datetime, timedelta
import time
import psutil
import signal
import sys

class WebInterface:
    def __init__(self):
        self.jean = "NotX"
    
    def open(self, website):
        if "http" not in website:
            website = f"http://{website}"
        run_cprogram(f'./Scripts/open_website {website}')

webbrowser = WebInterface()

def run_cprogram(path):
    if "./" not in path:
        path = f"./{path}"
    os.system(f"{path}")

def cprogram(path):
    threading.Thread(target=run_cprogram, args=(path,)).start()

def sherlock(args):
    os.system(f'./Scripts/sherlock {args}')

def timed_shutdown():
    print("59 minute timed shutdown active.")
    #time.sleep(3540)
    time.sleep(6)
    e = 1
    while True:
        try:
            sys.exit()
            quit()
        except:
            pass

def shutdown_handler(signal, frame):
    ShutdownIndicator = 1

    while True:
        ShutdownSafely()
        sys.exit()

def remove_from_list(variable, list):
    new_list = []
    for item in list:
        if item != variable:
            new_list.append(item)
    return new_list

# Internal functions
def check_network_status():
    while True:
        if not psutil.net_if_stats()['eth0'].isup:  # Change 'wlan0' to your network interface
            print("Network disconnected!")
            # Do something when network disconnects
        time.sleep(5)  # Adjust the sleep time as needed

def background_network():
    threading.Thread(target=check_network_status, args=()).start()

def loadconfig(file_path):
    with open(file_path, 'r') as json_file:
        config_data = json.load(json_file)
    return config_data

def saveconfig(file_path, dict):
    with open(file_path, 'w') as json_file:
        json.dump(dict, json_file, indent=4)

def play_notification_sound(sound_file_path):
    cprogram(f"./Scripts/audio_player {sound_file_path}")


def play_sound_in_background(notification_sound_file):
    play_notification_sound(notification_sound_file)

def DoFunction(intent_class):
    threading.Thread(target=DeployFunction, args=(intent_class,)).start()

def check_os():
    if sys.platform.startswith('linux'):
        print(f"Linux-based Operating System Detected.")
        return "Linux"
    elif sys.platform.startswith('darwin'):
        print(f"Caution: MacOS-based Operating System detected.")
        return "MacOS"
    elif sys.platform.startswith('win'):
        print(f"Caution: MS-DOS-based Operating System detected.")
        return "Windows"
    else:
        print(f"Caution: Unknown Operating System detected: {sys.platform}")
        return "Unknown"

OS = check_os()

def DeployFunction(intent_class):
    play_sound_in_background("AudioFiles/speechunderstood.mp3")
    intent_class = intent_class.get("tag")
    print(intent_class)
    if intent_class == "open-google":
        open_google()
    elif intent_class == "open-amazon":
        open_amazon()
    elif intent_class == "open-youtube":
        open_youtube()
    elif intent_class == "open-openai":
        open_openai()
    elif intent_class == "open-amazon-music":
        open_amazon_music()
    elif intent_class == "open-twitter":
        open_twitter()
    elif intent_class == "open-iplayer":
        open_iplayer()
    elif intent_class == "open-disney-plus":
        open_disney_plus()
    elif intent_class == "atom":
        open_atom()
    elif intent_class == "document":
        open_libreoffice()
    elif intent_class == "play-music":
        play_pause_music()
    elif intent_class == "pause-music":
        play_pause_music()
    elif intent_class == "next-music":
        next_music()
    elif intent_class == "previous-music":
        previous_music()
    elif intent_class == "change-response-type":
        change_response_setting()
    elif intent_class == "sleep-monitors":
        sleepPC()
    elif intent_class == "max-vol":
        maxvol()
    elif intent_class == "timer":
        set_timer()
    elif intent_class == "update-github":
        upload_to_github()
    elif intent_class == "download-github":
        download_from_github()
    elif intent_class == "unlock-screen":
        unlockPC()

    # Aesthetic shit idgaf

    elif intent_class == "blue":
        settings = loadconfig("./Settings/configuration.json")
        settings["colour"] = "BLUE"
        saveconfig("./Settings/configuration.json", settings)

    elif intent_class == "yellow":
        settings = loadconfig("./Settings/configuration.json")
        settings["colour"] = "YELLOW"
        saveconfig("./Settings/configuration.json", settings)

    elif intent_class == "red":
        settings = loadconfig("./Settings/configuration.json")
        settings["colour"] = "RED"
        saveconfig("./Settings/configuration.json", settings)
    
    # Sherlock

    elif intent_class == "sherlock":
        with open("short_term_memory/user_input.txt", "r") as file:
            usrinput = file.read()
        currentclass = loadconfig("short_term_memory/current_class.json")
#        currentclass = currentclass.get("intent_class")
        patterns = currentclass["patterns"]

        for pattern in patterns:
            usrinput = usrinput.replace(pattern, "")
        
        run_cprogram(f"./Scripts/sherlock {usrinput}")

# Website functions

def timer(time_in_seconds):
    time.sleep(time_in_seconds*60)
    play_sound_in_background("./AudioFiles/alarm_clock.mp3")

def set_timer():
    settings_config = loadconfig("./Settings/configuration.json")
    time_in_seconds = settings_config.get("default_timer")
    threading.Thread(target=timer, args=(time_in_seconds,)).start()

def background_alarm_clock():
    threading.Thread(target=reminders, args=()).start()

def reminders():
    all_reminders = loadconfig("./Settings/reminders.json")
    E = 1
    while True:
        current_time = datetime.now().time()
        formatted_time = current_time.strftime("%H:%M")
        for reminder in all_reminders["reminders"]:
            wake_time = reminder.get("time")
            if formatted_time == wake_time:
                os.system(f"amixer -D pulse sset Master 90%")
                tts(reminder.get("tag"))
                if reminder.get("type") == "alarm":
                    play_sound_in_background("./AudioFiles/alarm_clock.mp3")
                time.sleep(60)
                os.system(f"amixer -D pulse sset Master 65%")

def change_response_setting():
    settings_config = loadconfig("./Settings/configuration.json")
    if settings_config.get("response-type") == "random":
        settings_config["response-type"] = "fixed"
    else:
        settings_config["response-type"] = "random"
    saveconfig("./Settings/configuration.json", settings_config)

def open_google():
    webbrowser.open("https://www.google.co.uk")

def open_amazon():
    webbrowser.open("https://www.amazon.co.uk")

def open_youtube():
    webbrowser.open("https://www.youtube.co.uk")

def open_openai():
    webbrowser.open("https://chat.openai.co.uk")

def open_amazon_music():
    webbrowser.open("https://music.amazon.co.uk")

def open_twitter():
    webbrowser.open("https://www.twitter.co.uk")

def open_iplayer():
    webbrowser.open("https://www.bbc.co.uk/iplayer")

def open_disney_plus():
    webbrowser.open("https://www.disneyplus.co.uk/en-gb/select-profile")

def open_atom():
    os.system("atom-dev")

def open_libreoffice():
    os.system("libreoffice")

def upload_to_github():
    os.system("./upload")

def download_from_github():
    os.system("./download")

# Media functions

def play_pause_music():
    if OS == "Linux":
        cprogram("./Scripts/play-command")
    else:
        print("Operating system is not supported!")

def next_music():
    if OS == "Linux":
        cprogram("./Scripts/next-command")
    else:
        print("Operating system is not supported!")

def previous_music():
    if OS == "Linux":
        os.system("./Scripts/previous-command")
    else:
        print("Operating system is not supported!")

def sleepPC():
    if OS == "Linux":
        os.system("sleep 1; xset dpms force off")

def unlockPC():
    if OS == "Linux":
        os.system("loginctl unlock-session")

def mute():
    if OS == "Linux":
        print("Running on Linux")
        HostOS = "Linux"
        os.system(f"amixer -D pulse sset Master 0%")

    elif OS == "MacOS":
        print("Running on macOS")
        os.system("osascript -e 'set Volume 0'")

def maxvol():
    if OS == "Linux":
        print("Running on Linux")
        HostOS = "Linux"
        os.system(f"amixer -D pulse sset Master 100%")

    elif OS == "MacOS":
        print("Running on macOS")
        os.system("osascript -e 'set Volume 10'")

def speak(ResponseOutput):
    words = loadconfig("./Personality/pronounciation.json")
    for word in words["words"]:
        if word.get("word") in ResponseOutput:
            ResponseOutput = ResponseOutput.replace(word.get("word"), word.get("pronounce"))
    run_cprogram(f'./Utilities/tts "{ResponseOutput}"')

def save_speak(ResponseOutput):
    words = loadconfig("./Personality/pronounciation.json")
    for word in words["words"]:
        if word.get("word") in ResponseOutput:
            ResponseOutput = ResponseOutput.replace(word.get("word"), word.get("pronounce"))
    run_cprogram(f'./Utilities/tts_to_file "{ResponseOutput}"')

def tts(ResponseOutput):
    threading.Thread(target=speak, args=(ResponseOutput,)).start()

def mp3_tts(ResponseOutput):
    threading.Thread(target=save_speak, args=(ResponseOutput,)).start()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 functions.py <intent_class_json>")
        sys.exit(1)

    intent_class_json = sys.argv[1]

    try:
        intent_class = json.loads(intent_class_json)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        sys.exit(1)

    DoFunction(intent_class)

if __name__ == "__main__":
    main()