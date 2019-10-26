#include <stdio.h>
#include <cs50.h>

int main(void)
{
    float n;
    do
    {
        n = get_float("How much change do I owe you?: ");
    }
    while (n < 0);

    for (int change = n * 100; change >= 25; change -= 25)
    {
        printf("%i\n", change);
    }
}