#include <iostream>
#include <SFML/Audio.hpp>
#include <SFML/System.hpp>
#include <cstdlib> // For std::system

// Function to convert MP3 to WAV using ffmpeg
bool convertMP3toWAV(const std::string& mp3File, const std::string& wavFile) {
    std::string command = "ffmpeg -i \"" + mp3File + "\" \"" + wavFile + "\"";
    // Redirect output to /dev/null or NUL
    int result = std::system((command + " > /dev/null 2>&1").c_str());
    return result == 0; // Check if conversion was successful
}

int main(int argc, char* argv[]) {
    // Check if an MP3 file path is provided as argument
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <mp3_file_path>\n";
        return 1;
    }

    std::string mp3FilePath = argv[1];
    std::string wavFilePath = "temp.wav"; // Temporary WAV file

    // Convert MP3 to WAV
    if (!convertMP3toWAV(mp3FilePath, wavFilePath)) {
        std::cerr << "Failed to convert MP3 to WAV\n";
        return 1;
    }

    // Create a sound buffer and load the temporary WAV file
    sf::SoundBuffer buffer;
    if (!buffer.loadFromFile(wavFilePath)) {
        std::cerr << "Failed to load audio file\n";
        return 1;
    }

    // Create a sound instance and set its buffer
    sf::Sound sound;
    sound.setBuffer(buffer);

    // Play the audio
    sound.play();

    // Wait for the audio to finish playing
    while (sound.getStatus() == sf::Sound::Playing) {
        sf::sleep(sf::milliseconds(100));
    }

    // Delete the temporary WAV file
    std::remove(wavFilePath.c_str());

    return 0;
}
