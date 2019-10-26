#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(int argc, string argv[])
{
    // Finding correct key
    int digit = 0;
    if (argc == 2)
    {
        // Getting input string
        string s = argv[1];

        // Finding the length of the string
        int c = strlen(s);

        // split input string into digits
        char chr[c];
        int dig_unit = 0;

        // Checking for numeric digits
        for (int i = 0; i < c; i++)
        {
            chr[i] = s[i];
            if (isdigit(chr[i]) == 0)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
            else
            {
                dig_unit = (int)(chr[i] - '0');
                dig_unit *= pow(10, c - i - 1);
                digit = dig_unit + digit;
            }
            printf("%c\n",chr[i]);
        }
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    printf("%i\n",digit);
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
            int ans = count + digit;
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
            int ans = count + digit;
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
    }
    printf("ciphertext: %s\n", p_tx);
}

