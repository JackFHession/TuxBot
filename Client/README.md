<h1> The Janex Assistant </h1>

<h3> Introduction </h3>

<p> The Janex Assistant is a Natural Language AI assistant, primarily designed for Ubuntu Linux, which can listen and understand your commands.</p>
<p> Using Natural Language Processing, powered by the Janex Ultimate library, it can understand your intentions and act accordingly. </p>
<p> It works by taking in your input, either via text or voice, passing your input through a server-side Neural Network and enabling it to predict the category which your command falls within. E.g. "Please can you open Google" Janex then determines that it has a close cosine array to the category which is defined by "Open Google" and "Start up Google" commands. </p>

<h3> Installation </h3>

<p> The only binary I have compiled works for the Ubuntu OS. It is added to the 'Releases' section, always choose the latest full release for the most updated features. If you're not on Linux, you can download the .py file and run that, it should work but don't be surprised if it doesn't. </p>

<p> Simply download the executable, then allow it to function via </p>

```bash
sudo chmod +x '~/Downloads/Linux_Janex_Installer.run'
```

<p> Then just run the executable in terminal, which will bring up the GUI installer wizard. </p>

<h3> What can it do? </h3>

The Janex Assistant is capable of performing various tasks and providing assistance in different areas. Some of its functionalities include:

- **Opening Specific Websites/Applications:**
    - Open Google
    - Open Amazon
    - Open YouTube
    - Open Twitter
    - Open OpenAI
    - Open Amazon Music
    - Open Disney Plus

- **Controlling Media Playback:**
    - Pause music
    - Play music
    - Skip to the next song
    - Play the previous song

- **Adjusting System Settings:**
    - Max out the volume
    - Mute the volume
    - Sleep monitors
    - Unlock screens

- **Customizing Assistant's Appearance:**
    - Change response type (fixed/random)
    - Change color to blue/yellow/red

- **Technical Assistance:**
    - Help with technology
    - Update GitHub repository
    - Download GitHub updates
    - Search for any username through a number of social medias (via Sherlock)

- **Engaging in Small Talk:**
    - Greet
    - Respond to inquiries about well-being
    - Respond to expressions of gratitude
    - Bid farewell
    - Provide weather information
    - Discuss weekend plans
    - Offer movie recommendations
    - Share jokes
    - Discuss pets, hobbies, favorite movies, and more

- **Providing Information:**
    - Respond to FAQs related to programming, making friends, resolving family disputes, popular TV shows, video games, dealing with loneliness, managing stress, improving productivity, and more

- **Responding to Specific Inquiries:**
    - Provide information about Marvel characters and Doctor Who characters
    - Perform comparative analysis
    - Perform calculations based on user input

Please note that the Janex Assistant's capabilities are continually evolving, and new features may be added in future updates.

### Janex NLU Personal Assistant Installer

#### Overview

The Janex NLU Personal Assistant Installer script automates the installation process for the Janex NLU (Natural Language Understanding) Personal Assistant application. It provides a graphical user interface (GUI) for users to specify the installation directory and initiates the installation process with a single click.

#### Installation Steps

1. **Download the Script:** Download the `install_janex.py` script from the repository.
2. **Run the Script:**
   - Execute the script using Python 3.
3. **User Interface:**
   - The script launches a GUI window titled "NLU Personal Assistant - Installer".
   - Enter the desired installation directory in the provided field.
4. **Installation:**
   - Click the "Install" button to initiate the installation process.
   - The script downloads the Janex application from GitHub, extracts it to the specified directory, and installs dependencies.
5. **Completion:**
   - Upon successful installation, a message box confirms the completion.

### Credit where credit's due

1. This program's AI runs via the JanexUltimate library, which can be found via my profile.
2. An integrated tool which is based on Sherlock, many thanks to https://github.com/sherlock-project/sherlock
