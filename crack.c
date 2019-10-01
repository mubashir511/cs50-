#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <crypt.h>

int main(int argc, string argv[])
{
    // hash value of passaward
    string hash_old = "abBZmQBTazHcs";
    // Finding correct key
    if (argv[1] == NULL)
    {
        printf("Usage: ./crack password");
        return 1;
    }
    // Getting input string
    string s = argv[1];
    // Finding the length of the string
    int c = strlen(s);
    // If only one argument is present
    if ((argc == 2) && (c <= 5))
    {
        // Checking for numeric digits
        for (int i = 0; i < c; i++)
        {
            if (isdigit(s[i]) == 0)
            {
                if (((s[i] >= 'a') && (s[i] <= 'z')) || ((s[i] >= 'A') && (s[i] <= 'Z')))
                {
                    s[i] = s[i] + 0;
                }
                else
                {
                    printf("invalid keyword\n");
                    return 1;
                }
            }
            else
            {
                printf("Usage: ./crack password\n");
                return 1;
            }
        }
    }
    else
    {
        printf("Usage: ./crack password\n");
        return 1;
    }
    // Computing hash value of the give valu
    string hash_new = crypt(s, "ab");
    // Comparing both hashes
    if (strcmp(hash_old, hash_new) == 0)
    {
        printf("passward: %s\n", s);
        return 0;
    }
    else
    {
        printf("your passward is incorrect\n");
        return 0;
    }

}

