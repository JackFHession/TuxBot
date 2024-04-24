import tkinter as tk
import tkinter.messagebox as messagebox
import os
import shutil
import sys
import subprocess

class Downloader:
    def __init__(self, download_directory, installation_directory):
        self.download_directory = download_directory
        self.installation_directory = installation_directory

    def install_dependencies(self):
        commands = [
            "cd ~/.Janex-Assistant-Frontend && mkdir -p Virtual_Environment",
            "cd ~/.Janex-Assistant-Frontend/Virtual_Environment && python3 -m venv NLU_VE"]

        # Execute the commands
        for cmd in commands:
            subprocess.run(cmd, shell=True, executable="/bin/bash")
        
        os.system(". ~/.Janex-Assistant-Frontend/Virtual_Environment/NLU_VE/bin/activate && python3 -m pip install -r ~/.Janex-Assistant-Frontend/Setup/requirements.txt")

    def create_desktop_entry(self):
        if sys.platform.startswith('linux'):
            print("Linux-based Operating System Detected.")
            os.system("wget -P ~/ https://github.com/ChronoByte404/Janex-Assistant-Frontend/raw/main/Installers/Janex_Launcher_Ubuntu.program")
            desktop_entry = f'''[Desktop Entry]
    Name=NLU Assistant
    Exec={os.path.expanduser("~/Janex_Launcher_Ubuntu.program")}
    Icon={os.path.join(self.installation_directory, 'images', 'icon.png')}
    Type=Application
    Categories=Utility;'''

        elif sys.platform.startswith('win'):
            print("Windows Operating System Detected.")
            os.system("wget -P C:/Temp/ https://github.com/ChronoByte404/Janex-Assistant-Frontend/raw/main/Installers/Janex_Launcher_Windows.exe")
            # No need for chmod on Windows

            desktop_entry = ''  # No desktop entry for Windows currently

        else:
            print("Unsupported platform.")
            return

        desktop_path = os.path.join(os.path.expanduser('~'), '.local', 'share', 'applications', 'Janex-Assistant-Frontend.desktop')

        with open(desktop_path, 'w') as desktop_file:
            desktop_file.write(desktop_entry)

        print(f"Desktop entry created at: {desktop_path}")

    def download_and_extract(self):
        try:
            print("Removing existing installation (excluding Settings folder).")
            if os.path.exists(self.installation_directory):
                shutil.rmtree(self.installation_directory)

            print("Downloading zip.")
            os.system(f"cd {self.download_directory} && wget https://github.com/ChronoByte404/Janex-Assistant-Frontend/archive/refs/heads/main.zip -O Janex-Assistant-Frontend.zip")

            print("Extracting zip.")
            os.system(f"unzip -o {self.download_directory}/Janex-Assistant-Frontend.zip -d ~/ && cd ~/ && mv -f ./Janex-Assistant-Frontend-main ./.Janex-Assistant-Frontend")

            print("Creating executable.")

            NLUAssistantInfo = ""

            print("Installing dependencies and configuring virtual environment.")
            self.install_dependencies()

            messagebox.showinfo("Installation Complete", "NLU Personal Assistant has been installed successfully!")
            self.create_desktop_entry()  # Call to create desktop entry
            sys.exit()
        except Exception as e:
            messagebox.showerror("Installation Failed", f"An error occurred during installation: {str(e)}")


class App:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("NLU Personal Assistant - Installer")
        width, height = 324, 228
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

    def create_widgets(self):
        # Entry widget for directory
        default_directory = '~/.Janex-Assistant-Frontend'
        self.directory_entry = tk.Entry(self.root, bg="#ffffff", fg="#333333", justify="center")
        self.directory_entry.insert(tk.END, default_directory)
        self.directory_entry.place(x=30, y=90, width=260, height=30)

        # Entry widget for assistant name
        self.assistant_name_entry = tk.Entry(self.root, bg="#ffffff", fg="#333333", justify="center")
        self.assistant_name_entry.insert(tk.END, "NLU Assistant")
        self.assistant_name_entry.place(x=30, y=140, width=260, height=30)

        # Install button
        install_button = tk.Button(self.root, text="Install", command=self.install_action, bg="#01aaed", fg="#000000", justify="center")
        install_button.place(x=220, y=190, width=71, height=30)

        # Label
        label = tk.Label(self.root, text="Install your own Janex Personal Assistant", fg="#333333", justify="center")
        label.place(x=30, y=30, width=280, height=30)

    def install_action(self):
        directory = self.directory_entry.get()
        downloader = Downloader("~/Downloads", directory)
        downloader.download_and_extract()
        downloader.install_dependencies()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
