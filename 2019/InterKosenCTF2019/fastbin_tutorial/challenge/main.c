#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#define MAX_LIST 5

char *flag;
char *address[3] = {NULL};

char *last_freed = NULL;

void setup(void)
{
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
  FILE *f = fopen("flag.txt", "r");
  flag = malloc(0x50);
  if (f == NULL) {
    puts("[WARN] Please report this bug to the author.");
    exit(1);
  }
  fread(flag, 1, 0x50, f);
  fclose(f);
  malloc(0x100); // assure no leak by freed FILE buffer
}

void show_list(void)
{
  printf("\n");
  printf(" ===== Your List =====\n");
  printf("   A = %p\n", address[0]);
  printf("   B = %p\n", address[1]);
  printf("   C = %p\n", address[2]);
  printf(" =====================\n\n");
}

void show_fastbin(void)
{
  int i;
  char *ptr;

  unsigned long x, y;
  x = (unsigned long)last_freed;
  
  printf(" +---- fastbin[3] ----+\n");
  printf(" | 0x%016lx |\n", x);
  printf(" +--------------------+\n");
  printf("           ||\n");
  printf("           \\/\n");

  for(i = 0; i < MAX_LIST; i++) {
    if (x == 0) {
      printf("(end of the linked list)\n");
      break;
    } else if (x + 0x10 == (unsigned long)address[0]) {

      memcpy(&x, address[0], 8);
      memcpy(&y, address[0] + 8, 8);
      printf(" +--------- A --------+\n");
      printf(" | 0x%016lx |\n", x);
      printf(" | 0x%016lx |\n", y);
      printf(" +--------------------+\n");
      
    } else if (x + 0x10 == (unsigned long)address[1]) {
      
      memcpy(&x, address[1], 8);
      memcpy(&y, address[1] + 8, 8);
      printf(" +--------- B --------+\n");
      printf(" | 0x%016lx |\n", x);
      printf(" | 0x%016lx |\n", y);
      printf(" +--------------------+\n");
      
    } else if (x + 0x10 == (unsigned long)address[2]) {
      
      memcpy(&x, address[2], 8);
      memcpy(&y, address[2] + 8, 8);
      printf(" +--------- C --------+\n");
      printf(" | 0x%016lx |\n", x);
      printf(" | 0x%016lx |\n", y);
      printf(" +--------------------+\n");
      
    } else if (x + 0x10 == (unsigned long)flag) {
      
      printf(" +------- flag! ------+\n");
      printf(" | THE FLAG IS HERE!! |\n");
      printf(" +--------------------+\n");
      break;

    } else if (x == (unsigned long)flag) {

      printf(" +------- flag! ------+\n");
      printf(" | Oops! You forgot   |\n");
      printf(" |   the overhead...? |\n");
      printf(" +--------------------+\n");
      break;
      
    } else {
      
      printf("(maybe invalid address)\n");
      printf("(or unreferenced heap?)\n");
      break;
      
    }
    printf("           ||\n");
    printf("           \\/\n");
  }

  if (i == MAX_LIST) {
    printf("  (and more links...)\n");
  }
  
  printf("\n");
}

int getid(char *choice)
{
  printf("Which one? (A / B / C): ");
  scanf("%2s", choice);
  if (strcmp(choice, "A") == 0) {
    return 0;
  }
  if (strcmp(choice, "B") == 0) {
    return 1;
  }
  if (strcmp(choice, "C") == 0) {
    return 2;
  }
  printf("Invalid choice.\n");
  return -1;
}

void push_to_fastbin(int index)
{
  last_freed = address[index] - 0x10;
}

void pop_from_fastbin(int index)
{
  if (last_freed) {
    char* x;
    memcpy(&x, last_freed + 0x10, 8);
    last_freed = x;
  }
}

void tutorial(void)
{
  char var[8];
  int choice;
  int index;
  
  while(1) {
    show_list();
    show_fastbin();

    printf("You can do [1]malloc / [2]free / [3]read / [4]write\n");
    printf("> ");
    if (scanf("%d", &choice) != 1) {
      // Added during the competition
      getc(stdin);
      puts("Invalid choice.");
      continue;
    }
    if (choice == 1) {
      
      index = getid(var);
      if (index == -1) continue;
      pop_from_fastbin(index);
      printf("[+] %s = malloc(0x50);\n", var);
      address[index] = (char*)malloc(0x50);
      
    } else if (choice == 2) {
      
      index = getid(var);
      if (index == -1) continue;
      printf("[+] free(%s);\n", var);
      free(address[index]);
      push_to_fastbin(index);
      
    } else if (choice == 3) {
      
      index = getid(var);
      if (index == -1) continue;
      printf("[+] printf(\"[+] %%s\\n\", %s);\n", var);
      printf("[+] %s\n", address[index]);

    } else if (choice == 4) {
      
      index = getid(var);
      if (index == -1) continue;
      printf("[+] read(STDIN_FILENO, %s, 0x10);\n", var);
      printf("> ");
      read(0, address[index], 0x10);
      printf("[+] OK.\n");
      // renew_fastbin(index);
      
    } else {
      
      printf("Invalid choice.\n");
      
    }
  }
}

int main(void)
{
  setup();
  printf("Welcome to Double Free Tutorial!\n");
  printf("In this tutorial you will understand how fastbin works.\n");
  printf("Fastbin has various security checks to protect the binary\n");
  printf("from attackers. But don't worry. You just have to bypass\n");
  printf("the double free check in this challenge. No more size checks!\n");
  printf("Your goal is to leak the flag which is located at %p.\n\n", flag);

  printf("[+] f = fopen(\"flag.txt\", \"r\");\n");
  printf("[+] flag = malloc(0x50);\n");
  printf("[+] fread(flag, 1, 0x50, f);\n");
  printf("[+] fclose(f);\n\n");

  puts("This is the initial state:");
  tutorial();
  
  return 0;
}
