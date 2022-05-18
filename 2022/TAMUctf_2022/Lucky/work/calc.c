#include<stdio.h>
#include<stdlib.h>

void main()
{
	long seed_num = 0;
	while(1){
		srand(seed_num);
		int key0 = rand() == 306291429;
		int key1 = rand() == 442612432;
		int key2 = rand() == 110107425;

		if(key0 && key1 && key2) {
			printf("seed_num is %ld\n", seed_num);
			break;
		}
		seed_num++;
	}

}
