#include <iostream>
#include <cstdlib>
#include <string>

int main(int argc, char *argv[]) {
    // Check if an argument is provided
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
        return 1;
    }

    // Get the filename from the argument
    std::string filename = argv[1];

    // Construct the command with the filename
    std::string command = "python3 ./Maintenance/training.py " + filename;

    // Execute the command and store the return code
    int returnCode = system(command.c_str());

    return returnCode; // Return the return code of the system command
}
