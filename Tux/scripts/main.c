#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc > 2) {
        fprintf(stderr, "Usage: %s [argument]\n", argv[0]);
        return 1;
    }

    char *argument;
    if (argc == 2) {
        // If an argument is provided, use it
        argument = argv[1];
    } else {
        // If no argument is provided, set a default value or leave it empty
        argument = ""; // You can set a default value here if needed
    }

    // Construct the command to run the Python script
    char command[100]; // Assuming a maximum command length of 100 characters
    sprintf(command, "python3 main.py %s", argument);

    // Execute the command
    int result = system(command);

    // Check if the command executed successfully
    if (result != 0) {
        fprintf(stderr, "Error executing Python script\n");
        return 1;
    }

    return 0;
}
