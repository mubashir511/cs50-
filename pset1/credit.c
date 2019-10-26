#include <cs50.h>
#include <stdio.h>
#include <math.h>
// Gets number from user
long get_num(void);
// Apply Luhn's Algorithum
void luhn_Alg(long num);
// Check for correct card
void chk_card(int sum, int n);

int main(void)
{
    long num = get_num();
    luhn_Alg(num);
}

long get_num(void)
{
    long num;
    do
    {
        num = get_long("number: ");
    }
    while (num < 0);
    return num;

}

void luhn_Alg(long num)
{
    int m, n, o;
    int sw = 0;
    int sum = 0;
    int s = 0;
    int sm = 0;
    do
    {
        // Split long number into digits
        // Taking mod of number
        m = num % 10;
        // separating alternate digits
        if (sw == 0)
        {
            // Sum of the digits that weren’t multiplied by 2
            s += m;
            sw = 1;
        }
        else
        {
            // Multiply every other digit by 2
            // Starting with the number’s second-to-last digit
            m *= 2;
            if (m < 10)
            {
                sm += m;
            }
            else
            {
                do
                {
                    o = m % 10;
                    m /= 10;
                    sm += o;
                }
                while (m > 0);
            }
            sw = 0;
        }
        // Finding the first digit of the number
        if (num < 10)
        {
            n = num;
        }
        num /= 10;
    }
    while (num > 0);
    // Finding sum
    sum = s + sm;

    chk_card(sum, n);
}

void chk_card(int sum, int n)
{
    if ((sum % 10) == 0)
    {
        if (n == 3)
        {
            printf("AMEX\n");
        }
        else if (n == 5)
        {
            printf("MASTERCARD\n");
        }
        else if (n == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}


