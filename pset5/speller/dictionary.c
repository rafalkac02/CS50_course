// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <strings.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

int words_number = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 500000;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Set word's length extended by 1 for the null character
    int length = (strlen(word) + 1);
    
    // Temporary variable for lowercased words (to compare with dictionary)
    char tmp[length];

    for (int i = 0; i < (length - 1); i++)
    {
        char x = tolower(word[i]);
        tmp[i] = x;
    }
    tmp[length - 1] = '\0';

    // Hash the words from tmp variable
    int index = hash(tmp);

    // Compare words in text with words in dictionary
    for (node *cursor = table[index]; cursor != NULL; cursor = cursor->next)
    {
        if (strcasecmp(cursor->word, tmp) == 0)
        {
            return true;
        }
    }
    return false;
}



// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c = 0;

    while ((c = *word++))
    {
        hash = ((hash << 5) + hash) + c;
    }
    return hash % N;
}



// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];

    // Open the dictionary files
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)   // If error occurs
    {
        printf("Error! Can't open the file.\n");
        return false;
    }

    // Loop to scan the file
    while (fscanf(dict, "%s", word) != EOF)
    {
        // Increase words_number to use it on the function Size
        words_number++;

        // Memory allocation for a new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            printf("Error, not enough memory!\n");
            return false;
        }

        // Copy word into node
        strcpy(new_node->word, word);

        // Hash function returning an index
        int index = hash(new_node->word);

        // If likned list is empty, create a first node
        if (table[index] == NULL)
        {
            table[index] = new_node; 
            new_node->next = NULL;
        }
        // If linked list is not empty, insert a new node
        else
        {
            new_node->next = table[index]; 
            table[index] = new_node;
        }
    }
    fclose(dict);
    return true;
}



// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{

    return words_number;
}



// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Iterate over the hash table and each node to free them
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
        free(cursor);
    }
    return true;
}