#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

float scorings(string w);
int main(void)
{
    string read = get_string("Text: ");
    int score = (int) round(scorings(read));
    if (score < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (score > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %d\n", score);
    }
}

float scorings(string word)
{
    int letter = 0;
    int space = 0;
    int stop = 0;
    int len = strlen(word);
    for (int i = 0; i < len; i++)
    {
        if (word[i] == ' ')
        {
            space += 1;
        }
        else if (word[i] == '.' || word[i] == '!' || word[i] == '?')
        {
            stop += 1;
        }
        else if ((word[i] >= 'a' && word[i] <= 'z') || (word[i] >= 'A' && word[i] <= 'Z'))
        {
            letter += 1;
        }
    }
    int words = space + 1;
    float lw100 = ((float) letter / words) * 100;
    float sw100 = ((float) stop / words) * 100;
    float score = 0.0588 * lw100 - 0.296 * sw100 - 15.8;
    return score;
}
