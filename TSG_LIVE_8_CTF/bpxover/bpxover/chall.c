#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win() {
    char *argv[] = {"/bin/sh", NULL};
    execve("/bin/sh", argv, NULL);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    char buf[16];

    puts("hello :)");
    scanf("%s", buf);
    long x = strtoll(buf, NULL, 10);
    asm ("xor %0, %%rbp\n\t"
            :
    : "r" (x));

    return 0;
}
