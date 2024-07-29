#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " \"<text to speak>\"" << std::endl;
        return 1;
    }

    std::string textToSpeak = argv[1];

    // Construct the command to execute eSpeak with the provided text
    std::string command = "espeak \"" + textToSpeak + "\"";

    // Execute the command using system()
    int result = system(command.c_str());

    if (result != 0) {
        std::cerr << "Error executing eSpeak command" << std::endl;
        return 1;
    }

    return 0;
}
