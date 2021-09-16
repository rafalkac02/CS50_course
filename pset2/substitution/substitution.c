#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{

    // check for command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // check for correct key length
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // check for charachters validity
    for (int i = 0; i < 26; i++)
    {
        //check for non-alphabetic charakters
        if (!(isalpha(argv[1][i])))
        {
            printf("Key must be alphabetical only\n");
            return 1;
        }
        //check for repetition
        else
        {
            char letter = argv[1][i];
            if (strchr(argv[1] + 1 + i, letter))
            {
                printf("Letters in the key cannot be repeated.\n");
                return 1;
            }
        }
    }

    // input
    string plaintext = get_string("plaintext: ");

    // make an alphabet array
    char letter = 'a';
    int alphabet[26];
    for (int i = 0; i < 26; i++)
    {
        alphabet[i] = letter;
        letter++;
    }

    // output
    printf("ciphertext: ");

    int length = strlen(plaintext);

    for (int i = 0; i < length; i++)
    {
        // non-alphabetical charachters
        if (!(isalpha(plaintext[i])))
        {
            printf("%c", plaintext[i]);
        }

        // uppercase letter
        else if (isupper(plaintext[i]))
        {
            for (int j = 0; j < 26; j++)
            {
                if (toupper(alphabet[j]) == plaintext[i])
                {
                    printf("%c", toupper(argv[1][j]));
                }
            }
        }

        // lowercase letter
        else
        {
            for (int j = 0; j < 26; j++)
            {
                if ((alphabet[j]) == plaintext[i])
                {
                    printf("%c", tolower(argv[1][j]));
                }
            }
        }
    }
    printf("\n");
}