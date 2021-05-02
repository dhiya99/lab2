#include<stdio.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/wait.h>
#include<unistd.h>

int main(void)
{

        char name[60];

        for(int i=1;i<5;i++)
        {
                int lup=fork();

                if(lup==0)
                {
                        printf("\nEnter your name > ");
                        scanf("%s", name);
                        printf("Your name is %s \n", name);
                        exit(0);
                }

                else
                {
                        wait(NULL);
                        printf("Job is done.\n\n");
                }
        }

        return EXIT_SUCCESS;}

