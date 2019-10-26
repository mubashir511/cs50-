#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(int argc, string argv[])
{
    // Finding correct key
    if (argv[1] == NULL)
    {
        printf("Usage: ./vigenere key\n");
        return 1;
    }
    // Getting input string
    string s = argv[1];

    // Finding the length of the string
    int c = strlen(s);

    // Initiallizing an integer array for keys
    int key[c];
    int key_index = 0;

    // If only one argument is present
    if (argc == 2)
    {
        // Checking for numeric digits
        for (int i = 0; i < c; i++)
        {
            if (isdigit(s[i]) == 0)
            {
                if ((s[i] >= 'a') && (s[i] <= 'z'))
                {
                    key[i] = s[i] - 97;
                }
                else if ((s[i] >= 'A') && (s[i] <= 'Z'))
                {
                    key[i] = s[i] - 65;
                }
                else
                {
                    printf("invalid keyword\n");
                    return 1;
                }
            }
            else
            {
                printf("Usage: ./vigenere key\n");
                return 1;
            }
            printf("key: %i\n", key[i]);
        }
    }
    else
    {
        printf("Usage: ./vigenere key\n");
        return 1;
    }
    // Applying encryption
    // Asking Plain text
    string p_tx = get_string("plaintext: ");

    // Shifting letters in the string
    for (int j = 0; p_tx[j] != '\0'; j++)
    {
        // Shifting lowercase alphabets
        if ((p_tx[j] >= 'a') && (p_tx[j] <= 'z'))
        {
            int count = (int) p_tx[j];
            int chk_count = count - 1;
            int ans = count + key[key_index];
            for (int k = count; count <= ans; count++)
            {
                if (chk_count == 122)
                {
                    chk_count = 97;
                }
                else
                {
                    chk_count++;
                }
            }
            p_tx[j] = (char) chk_count;
        }
        // Shifting uppercase alphabets
        else if ((p_tx[j] >= 'A') && (p_tx[j] <= 'Z'))
        {
            int count = (int) p_tx[j];
            int chk_count = count - 1;
            int ans = count + key[key_index];
            for (int k = count; count <= ans; count++)
            {
                if (chk_count == 90)
                {
                    chk_count = 65;
                }
                else
                {
                    chk_count++;
                }
            }
            p_tx[j] = (char) chk_count;
        }
        // Ignore empty spaces
        else
        {
            key_index--;
        }
        // Changing key array index
        if (key_index == c - 1)
        {
            key_index = 0;
        }
        else
        {
            key_index++;
        }

    }
    printf("ciphertext: %s\n", p_tx);
}



