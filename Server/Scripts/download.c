#include <stdlib.h>

int main() {
    int result = system("git pull");
    if (result != 0) {
        // Handle the "exception" by stashing changes and trying again
        system("git stash");
        result = system("git pull");
    }
    return 0;
}