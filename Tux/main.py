from internal.core import *

if __name__ == "__main__":
    Mode = input("Mode (voice/text): ")
    if Mode.lower() == "text":
        Instance = Intel()
        while True:
            Instance.default_interface()
