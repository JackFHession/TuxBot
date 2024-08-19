#include <iostream>
#include <string>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " \"text to synthesize\"" << std::endl;
        return 1;
    }

    std::string text = argv[1];
    std::string command = "espeak \"" + text + "\" --stdout > ./AudioFiles/output.wav && lame ./AudioFiles/output.wav ./AudioFiles/output.mp3 && rm ./AudioFiles/output.wav";

    std::cout << "Synthesizing speech..." << std::endl;

    int result = system(command.c_str());

    if (result == 0) {
        std::cout << "Speech synthesized and saved as output.mp3" << std::endl;
    } else {
        std::cerr << "Error synthesizing speech" << std::endl;
    }

    return 0;
}