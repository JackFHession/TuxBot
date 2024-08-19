#include <iostream>
#include <string>
#include <vector>

int main(int argc, char* argv[]) {
    // Check if at least one command-line argument (excluding the program name) is provided
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " [python arguments]" << std::endl;
        return 1; // Return error code indicating incorrect usage
    }

    std::string pythonCommand = "cd Utilities && python3 sherlock";
    
    // Append all command-line arguments to the python command
    for (int i = 1; i < argc; ++i) {
        pythonCommand += " ";
        pythonCommand += argv[i];
    }

    // Execute the constructed command
    system(pythonCommand.c_str());

    return 0; // Return success
}
