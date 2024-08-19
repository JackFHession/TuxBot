#include <iostream>
#include <cstdlib> // For std::system

int main(int argc, char *argv[]) {
    // Check if at least one command-line argument (the program name itself) is provided
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <website_url>" << std::endl;
        return 1; // Exit with an error code
    }

    // The first command-line argument (argv[1]) is the website URL
    std::string url = argv[1];

    // Build the command to open the URL using xdg-open
    std::string command = "xdg-open " + url;

    // Open the URL in the default web browser
    std::system(command.c_str());

    return 0;
}
