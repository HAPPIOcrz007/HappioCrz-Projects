// project:  cash: easier one
// objective:calculating minimum number of coins to be used for payment
#include <cs50.h>
#include <stdio.h>
// libraries included
int main(void)
{
    int owed = -1;
    // initialised owed amount --> default negative
    do
    {
        owed = get_int("Change owed: ");
    }
    while (owed < 0);
    // ensured user enter value positive or zero
    int coins = 0;
    while (owed >= 25)
    {
        owed = owed - 25;
        coins++;
    }
    // by greedy algorithms 25's calculation done
    while (owed >= 10)
    {
        owed = owed - 10;
        coins++;
    }
    // by greedy algorithms 10's calculation done
    while (owed >= 5)
    {
        owed = owed - 5;
        coins++;
    }
    // by greedy algorithms 5's calculation done
    while (owed >= 1)
    {
        owed = owed - 1;
        coins++;
    }
    // by greedy algorithms 1's calculation done
    printf("%i\n", coins);
    // output printed to the user
}
