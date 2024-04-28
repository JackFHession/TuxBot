import os

class layout_template:
    def __init__(self):
        self.path = ""

    def set_face(self, path):
        os.system("clear")
        with open(path, "r") as face:
            print(face.read())
        print("")
    
    def get_input(self):
        input_text = input("\nYou: ")
        return input_text

