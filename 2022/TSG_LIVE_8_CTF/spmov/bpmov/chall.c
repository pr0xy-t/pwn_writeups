#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <time.h>

void win() {
    char *argv[] = {"/bin/sh", NULL};
    asm volatile
    (
        "syscall"
        :
        : "a"(59), "D"("/bin/sh"), "S"(argv), "d"(NULL)
        : "rcx", "r11", "memory"
    );
}

void stop_a_little() {
    sleep(rand()%2);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    srand(time(NULL));

    long x;
    char buf[40] = {0};
    puts("hello");

    read(0, buf, 39);
    x = strtoll(buf, NULL, 10);
    asm ("mov %0, %%rsp\n\t"
            :
    : "r" (x));

    stop_a_little();
    read(0, buf, 39);
    printf("bye, %s", buf);

    return 0;
}
