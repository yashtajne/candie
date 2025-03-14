#include <stddef.h>

extern void greet(const char *name);

int main() {

    const char *friends[] = {
        "Chandler",
        "Joey",
        "Monica",
        "Rachel",
        "Phoebe"
    };

    for (size_t i; i < sizeof(friends) / sizeof(friends[0]); i++) {
        greet(friends[i]);
    }

    return 0;
}