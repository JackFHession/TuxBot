from Internal.framework import *
from Utilities.functions import *
from backgroundstuff.alarm_client import *

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QDialog, QVBoxLayout, QComboBox, QMessageBox

Instance = Interface()
Config = loadconfig("./Settings/config.json")

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Janex Assistant")
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(600, 400)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 10, 580, 300)
        self.text_edit.setStyleSheet("background-color: black; color: grey;")
        self.text_edit.setReadOnly(True)  # Set read-only

        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(10, 320, 400, 30)
        self.input_field.returnPressed.connect(self.handle_input)

        self.mode_combo = QComboBox(self)
        self.mode_combo.setGeometry(420, 320, 170, 30)
        self.mode_combo.addItems(["Text", "Audio"])  # Add your modes here
        self.mode_combo.currentTextChanged.connect(self.update_mode)

        self.mode = "text"  # Variable to store selected mode

    def update_mode(self, mode_text):
        if mode_text == "Text":
            self.mode = "text"
        elif mode_text == "Audio":
            self.mode = "audio"
        self.text_edit.append(f"{Config.get('UIName')}: Communication mode switched to {mode_text}")

    def handle_input(self):
        text = self.input_field.text()
        self.text_edit.append(f"You: {text}")
        self.input_field.clear()  # Clear the input field

        self.process_input(text)

    def audio_mode(self):
        while self.mode.lower() == "audio":
            try:
                Instance.VoiceCommand()
                ResponseOutput, intent_class = Instance.send_audio()
                DoFunction(intent_class)
                tts(ResponseOutput)
                # Update GUI using signal
                self.text_edit.append(f"{Config.get('UIName')}: {ResponseOutput}")
            except Exception as e:
                error_message = f"Error: {e}"
                print(error_message)
                QMessageBox.critical(self, "Error", error_message)
                break  # Exit the loop on error
    
    def process_input(self, text):
        if self.mode == "audio":
            threading.Thread(target=self.audio_mode).start()

        elif self.mode == "text":
            # Handle text input
            try:
                Instance.send(text)
                ResponseJson = loadconfig("./local_memory/current_class.json")
                ResponseOutput, intent_class = ResponseJson.get("response"), ResponseJson.get("intent_class")
                DoFunction(intent_class)
                tts(ResponseOutput)
                self.text_edit.append(f"{Config.get('UIName')}: {ResponseOutput}")
            except Exception as e:
                error_message = f"Error: {e}"
                print(error_message)
                QMessageBox.critical(self, "Error", error_message)
        
    def select_mode(self):
        mode_dialog = ModeDialog(self)
        if mode_dialog.exec_() == QDialog.Accepted:
            self.mode = mode_dialog.get_selected_mode()

class ModeDialog(QDialog):
    def __init__(self, parent=None):
        super(ModeDialog, self).__init__(parent)
        self.setWindowTitle("Select Mode")
        layout = QVBoxLayout()

        self.audio_button = QPushButton("Audio Mode")
        self.text_button = QPushButton("Text Mode")

        layout.addWidget(self.audio_button)
        layout.addWidget(self.text_button)

        self.audio_button.clicked.connect(self.select_audio_mode)
        self.text_button.clicked.connect(self.select_text_mode)

        self.selected_mode = None

        self.setLayout(layout)

    def select_audio_mode(self):
        self.selected_mode = "audio"
        self.accept()

    def select_text_mode(self):
        self.selected_mode = "text"
        self.accept()

    def get_selected_mode(self):
        return self.selected_mode

if __name__ == "__main__":
    threading.Thread(target=send_request_in_background).start()
    app = QApplication(sys.argv)
    window = MyWindow()
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        window.mode = mode
    window.show()
    sys.exit(app.exec_())
