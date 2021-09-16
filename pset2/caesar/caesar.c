#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>


int main(int argc, string argv[])
{
    // check how many command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // check if all characters are digits
    for (int i = 0, n = strlen(argv[1]); i < n;)
    {
        if (isdigit(argv[1][i]))
        {
            i++;
        }
        else
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // treat key as an integer
    int k = atoi(argv[1]);

    // input
    string pt = get_string("plaintext: ");

    // output
    printf("ciphertext: ");

    // encrypt message
    for (int i = 0, n = strlen(pt); i < n; i++)
    {
        // uppercase letters
        if (isupper(pt[i]))
        {
            printf("%c", (pt[i] - 64 + k) % 26 + 64);

        }

        // lowercase letters
        else if (islower(pt[i]))
        {
            printf("%c", (pt[i] - 96 + k) % 26 + 96);
        }

        // non-alphabetic
        else
        {
            printf("%c", pt[i]);
        }
    }

    printf("\n");
    return 0;
}