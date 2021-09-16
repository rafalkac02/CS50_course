#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>


int main(void)
{
    // set up variables
    float letters = 0;
    float spaces = 0;
    float sentences = 0;

    // prompt for text
    string text = get_string("Text: ");


    // count letters
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }

    // count words (spaces)
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == ' ')
        {
            spaces++;
        }
    }
    int words = spaces + 1;

    // count sentences
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }


    // plug values into formula
    float L = (letters / words) * 100;    // L is average number of letters per 100 words
    float S = (sentences / words) * 100;    // S is average number of sentences per 100 words


    float index = 0.0588 * L - 0.296 * S - 15.8;

    // final result
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %.0f\n", index);
    }
}