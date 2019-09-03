#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float cash;
    int q25 = 0; 
    int q10 = 0; 
    int q5 = 0; 
    int q1 = 0;
    // Get dollar value from user 
    do
    {
        cash = get_float("change: ");
    }
    while (cash < 0);
    // Convert dollar value into cents 
    int cents = cash * 100;
    // Checking for quarters
    if ((cents / 25) >= 1)
    {
        q25 = cents / 25; 
        cents = cents % 25; 
    }
    // Checking for dimes
    if ((cents / 10) >= 1)
    {
        q10 = cents / 10;
        cents = cents % 10; 
    }
    // Checking for nickels 
    if ((cents / 5) >= 1)
    {
        q5 = cents / 5;
        cents = cents % 5; 
    } 
    // Checking for pennies
    if ((cents / 1) >= 1)
    {
        q1 = cents / 1;
    }
    // Taking sum all the avaiable type of coins 
    int coins = q25 + q10 + q5 + q1;
    printf("coins: %i\n", coins);
}

