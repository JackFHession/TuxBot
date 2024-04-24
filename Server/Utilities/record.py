import pyaudio
import wave
import numpy as np
from scipy.io import wavfile
import os

class Audio:
    def __init__(self):
        self.e = 0
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 1
        self.fs = 44100
        self.seconds = 2.8
        self.filename = "short_term_memory/audio.wav"
        self.threshold = 6000

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

        stream.stop_stream()
        stream.close()

        p.terminate()

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(frames))
        wf.close()

if __name__ == "__main__":
    Instance = Audio()
    Instance.VoiceCommand()