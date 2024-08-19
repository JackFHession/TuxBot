#include <iostream>
#include <cstdlib>
#include <string>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " 'Text to classify'" << std::endl;
        return 1;
    }

    std::string command = "python3 ./AI/main.py ";
    command += '"';
    command += argv[1];
    command += '"';
    int status = system(command.c_str());

    if (status != 0) {
        std::cerr << "Error executing Python program" << std::endl;
        return 1;
    }

    return 0;
}
