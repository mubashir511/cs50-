// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <math.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 25

// Represents a node in a hash table
typedef struct node
{
    char data[LENGTH + 1];
    struct node *next;
}
node;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Dynamic array that carries the letters
char *node1 = NULL;

// Array that records the length of each word from start till end
long *word_strength = NULL;

// Quantity of individal alphabets
long letter_strength[N];

// How many words
long word_count = 1;

int start = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Dynamic array that carries the letters
    node1 = malloc(sizeof(LENGTH + 1) * word_count);

    // length of individual word
    int word_length = 0;

    // Array that records the length of each word from start till end
    word_strength = malloc(sizeof(long) * word_count);

    for (int i = 0; i < N; i++)
    {
        letter_strength[i] = 0;
    }

    // Checking words from the given dictionary file
    while (fscanf(file, "%s", word) != EOF)
    {
         int ascii = (int) word[0];
         int index;
         // Find which alphabet appears
         // small alphabets
         if (ascii >= 97 && ascii <= 122)
         {
            index = ascii % 97;
         }
         // Capital aphabets
         if (ascii >= 65 && ascii <= 90)
         {
            index = ascii % 65;
         }

        // Increase the quantity of that alphabet
        letter_strength[index] += 1;

        //printf("%s\n", word);

        // Get length of the word
        word_length = strlen(word);

        // Copy the length of the word in an array
        word_strength[word_count - 1] = word_length;

        // Copy word in another array
        strcpy(&node1[start], word);
        start += word_length;

        word_count++;

        // Allocate more space for word array
        node1 = realloc(node1, (sizeof(char) * LENGTH) * word_count);

        // Allocate more space for word-lenght array
        word_strength = realloc(word_strength, sizeof(long) * word_count);

    }
    /*for(int i = 0; i <= N; i++)
    {
        printf("%li\n", letter_strength[i]);
    }*/

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;

}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (word_count != 0)
    {
        return word_count - 1;
    }
    else
    {
       return 0;
    }

}

// Returns true if word is in dictionary else false
char *word_buffer = NULL;
char *check_word = NULL;

bool check(const char *word)
{
    printf("\n");
    int l = strlen(word);
    check_word = malloc(sizeof(char) * l);

    if (l > 45 || l < 1)
    {
        return false;
    }
    // Conver 'word' into lower case
    for (int i = 0; i < l; i++)
    {
        if (isalpha(word[i]) != 0)
        {
            check_word[i] = tolower(word[i]);
        }
        else
        {
            check_word[i] = word[i];
        }
    }
    printf("%s\n", check_word);

    long head = 0;
    long tail = 0;
    long from = 0;
    long to = 0;
    int result;

    int ascii = (int) check_word[0];
    int index;
    // Find which alphabet appears
    // small alphabets
    if (ascii >= 97 && ascii <= 122)
    {
        index = ascii % 97;
    }
    // Capital aphabets
    if (ascii >= 65 && ascii <= 90)
    {
        index = ascii % 65;
    }
    // find the index of first and last word starting with that letter
    // if 'a'
    if(index == 0)
    {
        head = 0;
    }
    else
    {
        for(int i = 0; i < index; i++)
        {
            head += letter_strength[i];
        }
    }
    tail = letter_strength[index] - 1;
    tail += head;

    for (int i = 0; i < head; i++)
    {
        from += word_strength[i];
    }
    for (int i = head; i <= tail; i++)
    {
        to += word_strength[i];
    }

    /*printf("head: %li\n", head);
    printf("tail: %li\n", tail);
    printf("from: %li\n", from);
    printf("to: %li\n", to);
    printf("index: %i\n", index);*/

    /*for (int i = 0; i <= 10; i++)
    {
        printf("%c", node1[from + i]);
    }*/

    // Find each word
    for (int i = head; i <= tail; i++)
    {
        word_buffer = malloc(sizeof(char) * word_strength[i]);

        for (int j = 0; j < word_strength[i]; j++)
        {
            //printf("%c", node1[from + j]);
            word_buffer[j] = node1[from + j];
        }
        //printf("%s\n", word_buffer);
        from += word_strength[i];

        result = strcasecmp(check_word, word_buffer);

        if (result == 0)
        {
            //printf("%s is present in the dictionary\n", word_buffer);
            return true;
        }
        word_buffer = NULL;
    }
    return false;
}


// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    free(node1);
    free(word_strength);
    free(word_buffer);
    free(check_word);
    return true;
}