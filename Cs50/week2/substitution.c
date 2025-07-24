#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

string cipher(string text, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];

    // Validate length
    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // Validate characters: must be alphabetic and non-repeating
    int seen[26] = {0};
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }

        int index = toupper(key[i]) - 'A';
        if (seen[index] == 1)
        {
            printf("Key must not contain repeated characters.\n");
            return 1;
        }
        seen[index] = 1;
    }

    string plaintext = get_string("plaintext: ");
    string ciphertext = cipher(plaintext, key);
    printf("ciphertext: %s\n", ciphertext);
}

// This function modifies the original string, which is allowed in CS50's get_string
string cipher(string text, string key)
{
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isupper(text[i]))
        {
            int index = text[i] - 'A';
            text[i] = toupper(key[index]);
        }
        else if (islower(text[i]))
        {
            int index = text[i] - 'a';
            text[i] = tolower(key[index]);
        }
        // Non-alphabetic characters remain unchanged
    }
    return text;
}
