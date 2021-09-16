#include <cs50.h>
#include <stdio.h>


int main(void)
{
    // prompt for valid imput
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);
    
    
    // loop through pyramid's rows
    for (int i = 0; i < height; i++)
    {
        // left-sided spaces
        int spaces = height - 1 - i;
        for (int j = 0; j < spaces; j++)
        {
            printf(" ");
        }
        
        // left-sided hashes
        for (int k = 0; k < i + 1; k++)
        {
            printf("#");
        }
        
        // gap 
        printf("  ");
        
        // right-sided hashes
        for (int l = 0; l < i + 1; l++)
        {
            printf("#");
        }
        
        // head to a new line
        printf("\n");
    }
}