// project:  mario easier one
// objective:making a half pyramid according to user input
#include <cs50.h>
#include <stdio.h>
// libraries included
int main(void)
{
    int pyHeight = 0;
    // initialised pyheight --> height of pyramid
    do
    {
        pyHeight = get_int("enter half pyramid height ");
    }
    while (pyHeight < 1);
    // ensured user input not less than 1
    for (int i = 1; i <= pyHeight; i++)
    {
        // generated row
        for (int j = pyHeight; j > 0; j--)
        {
            if (j > i)
            {
                printf(" ");
            }
            else if (j <= i)
            {
                printf("#");
            }
        }
        // built columns and filled hashes
        printf("\n");
        // moved to a new line
    }
}
