import whisper

class speech:
    def __init__(self):
        self.model = whisper.load_model("base.en")
        self.filename = "./short_term_memory/input_audio.wav"

    def transcribe(self):
        result = self.model.transcribe(f"{self.filename}")
        sentence = result["text"].strip()  # Trim leading and trailing spaces

        print(sentence)

        return sentence

if __name__ == "__main__":
    Instance = speech()
    Instance.transcribe()
