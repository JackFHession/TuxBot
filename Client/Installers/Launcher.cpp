#include <cstdlib>
#include <unistd.h>
#include <cstdio> // Include stdio.h for printf
#include <iostream>
using namespace std;

int main() {
    // Path to the virtual environment's activate script
    const char* activateScript = ".Janex-Assistant-Frontend/Virtual_Environment/NLU_VE/bin/activate";

    // Execute the shell command to source the activate script
    int status = system(". .Janex-Assistant-Frontend/Virtual_Environment/NLU_VE/bin/activate && cd ~/.Janex-Assistant-Frontend && python3 main.py");

    if (status != 0) {
        // Handle error if the command failed
        return 1;
    }

    // Example usage of printf
    printf("Virtual environment activated successfully!\n");

    // Execute terminal command
    system("cd ~/.Janex-Assistant-Frontend && python3 main.py");

    // Example usage of printf
    printf("Terminal command executed.\n");

    return 0;
}
