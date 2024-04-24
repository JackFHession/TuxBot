#include <stdlib.h>

int main() {
    system("git rm -rf --cached .");
    system("git add .");
    system("git add *");
    system("git commit -m 'Automation'");
    system("git push");
    return 0;
}
