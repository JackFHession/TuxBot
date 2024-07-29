import pyaudio
import wave
import numpy as np
from scipy.io import wavfile
import os

from Utilities.functions import *
import requests

class Interface:
    def __init__(self):
        self.config = loadconfig("./Settings/config.json")
        self.e = 0
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 1
        self.fs = 44100
        self.seconds = 2.8
        self.filename = "local_memory/audio.wav"
        self.threshold = 6000
    
    def send(self, text):
        os.system(f'./Scripts/send_request {self.config.get("IP")} "{text}"')
        with open("./short_term_memory/user_input.txt", "w") as file:
            file.write(text)
    
    def send_audio(self):
        url = self.config.get("SecondIP")
        files = {'file': open('local_memory/audio.wav', 'rb')}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            response_data = response.json()
            
            ResponseOutput = response_data.get("ResponseOutput")
            intent_class = response_data.get("intent_class")

            with open("./short_term_memory/user_input.txt", "w") as file:
                file.write("None")

            return ResponseOutput, intent_class
        else:
            print("Failed to receive a valid response from the server.")


    def VoiceCommand(self):
        p = pyaudio.PyAudio()
        os.system("clear")
        print('Listening')

        stream = p.open(format=self.sample_format,
                        channels=self.channels,
                        rate=self.fs,
                        frames_per_buffer=self.chunk,
                        input=True)

        frames = []
        while True:
            data = stream.read(self.chunk)
            signal = np.frombuffer(data, dtype=np.int16)
            amplitude = np.max(signal)
            if amplitude > self.threshold:
                break

        try:
            notification_sound_file = 'AudioFiles/speechdetected.mp3'
            play_sound_in_background(notification_sound_file)
        except:
            pass

        print('Recording')

        for i in range(0, int(self.fs / self.chunk * self.seconds)):
            print(i)
            data = stream.read(self.chunk)
            frames.append(data)
        
        print("Recording finished.")

        try:

            stream.stop_stream()
            stream.close()

            p.terminate()

            wf = wave.open(self.filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(frames))
            wf.close()
        
        except Exception as e:
            with open("./logs/error", "w") as f:
                f.write(Exception)
