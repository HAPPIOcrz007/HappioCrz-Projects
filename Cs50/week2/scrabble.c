#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int scorings(string w);
int main(void)
{
    string s1 = get_string("Player 1: ");
    string s2 = get_string("Player 2: ");
    printf("\n");
    int s1s = scorings(s1);
    int s2s = scorings(s2);
    if (s1s > s2s)
    {
        printf("Player 1 wins!\n");
    }
    else if (s1s < s2s)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int scorings(string word)
{
    int score = 0, scoring[] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                                1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    for (int i = 0, l = strlen(word); i < l; i++)
    {
        if (word[i] >= 'a' && word[i] <= 'z')
        {
            int a = word[i] - 'a';
            score += scoring[a];
        }
        else if (word[i] >= 'A' && word[i] <= 'Z')
        {
            int a = word[i] - 'A';
            score += scoring[a];
        }
    }
    return score;
}
