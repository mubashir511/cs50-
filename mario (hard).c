#include <cs50.h>
#include <stdio.h>

########## mario hard #########

int main(void)
{
    int i;
    int j;
    int k;
    int height;
    int key=0;
    
    while(key==0)
    	{
        height = get_int("height: ");

	// Check if height is between 1 and 8         
	if ((height>=1)&&(height<=8)) 
        {
	    // Terminating loop	
            key=1; 
        }  
    }
    for (i=1; i<=height; i++)
    {
        for (j=1; j<=height; j++)
        {
            if (j<=(height-i))
            {
                printf(" ");
            }
            else 
            {
                printf("#");
            }
        }
        printf("  ");
        for(k=1; k<=i; k++)
        {
            printf("#");
        }
        printf("\n");
    }
    
}



