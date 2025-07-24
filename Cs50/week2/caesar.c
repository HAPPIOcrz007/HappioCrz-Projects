#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
// all libraries added
string cipher(string text, int key);
int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // checked if total number of arguments is 2 -> file + agument 1 exist
    int key = 0;
    for (int i = 0, l = strlen(argv[1]); i < l; i++)
    {
        if (argv[1][i] >= '0' && argv[1][i] <= '9')
        {
            key = key * 10 + (argv[1][i] - '0');
        }
        else
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    // checked if the second argument consist only of digits

    printf("ciphertext: %s", cipher(get_string("plaintext:  "), key));
    // asking the user for input and calling cipher function with the key
    // getting the return from cipher function and giving the output
    printf("\n");
}
string cipher(string text, int key)
// cipher function
{

    for (int i = 0, l = strlen(text); i < l; i++)
    {
        if (text[i] >= 'A' && text[i] <= 'Z')
        {
            text[i] = ((text[i] - 'A' + key) % 26) + 'A';
        }
        else if (text[i] >= 'a' && text[i] <= 'z')
        {
            text[i] = ((text[i] - 'a' + key) % 26) + 'a';
        }
    }
    return text;
}
