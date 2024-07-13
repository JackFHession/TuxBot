#include <iostream>
#include <cstdlib>
#include <string>
#include <cctype>  // For toupper function

int main() {
    char interface[256];
    std::cout << "\nAre you running client or server? ";
    std::cin >> interface;

    // Convert the first letter to uppercase
    interface[0] = std::toupper(interface[0]);

    // Construct the command string
    std::string command = "cd ";
    command += interface;
    command += " && python3 main.py";
    
    // Execute the command
    system(command.c_str());
    
    return 0;
}
