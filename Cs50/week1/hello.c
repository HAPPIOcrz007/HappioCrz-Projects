// print hello followed by user input
#include <cs50.h>
#include <stdio.h>
// any file ending with .h is header file
// header file --> functionality coming with the code file

int main(void)
{
    string answer = get_string("What's your name? "); // asking the user for input
    printf("hello, %s\n", answer);                    // printing the output
}
