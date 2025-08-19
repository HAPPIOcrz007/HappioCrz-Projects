#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // grayscale = 0.3 * R + 0.59 * G + 0.11 * B
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int grayscale = (int) round(
                (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = grayscale;
            image[i][j].rgbtGreen = grayscale;
            image[i][j].rgbtBlue = grayscale;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // values may not be an integer, but each value could be rounded to the nearest integer.
    // if value > 255 or < 0 cap them at [0,255]
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int originalRed = image[i][j].rgbtRed;
            int originalGreen = image[i][j].rgbtGreen;
            int originalBlue = image[i][j].rgbtBlue;

            int sepiaRed =
                (int) round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            int sepiaGreen =
                (int) round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            int sepiaBlue =
                (int) round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);

            image[i][j].rgbtRed = (int) fmin(255, fmax(0, sepiaRed));
            image[i][j].rgbtGreen = (int) fmin(255, fmax(0, sepiaGreen));
            image[i][j].rgbtBlue = (int) fmin(255, fmax(0, sepiaBlue));
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // we will just for first try switch places
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE tempo = image[i][(width - 1) - j];
            image[i][(width - 1) - j] = image[i][j];
            image[i][j] = tempo;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Temporary array to store blurred image
    RGBTRIPLE temp[height][width];

    // Iterate through each pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumR = 0;
            int sumG = 0;
            int sumB = 0;
            int counter = 0;

            // Iterate through the 3x3 grid surrounding the current pixel
            for (int m = -1; m <= 1; m++) // m iterates over rows (-1, 0, 1)
            {
                for (int n = -1; n <= 1; n++) // n iterates over columns (-1, 0, 1)
                {
                    int ni = i + m;
                    int nj = j + n;

                    // Ensure the neighbor is within bounds
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        sumR += image[ni][nj].rgbtRed;
                        sumG += image[ni][nj].rgbtGreen;
                        sumB += image[ni][nj].rgbtBlue;
                        counter++;
                    }
                }
            }

            // Store the averaged color values in the temporary image
            temp[i][j].rgbtRed = (int) round((float) sumR / counter);
            temp[i][j].rgbtGreen = (int) round((float) sumG / counter);
            temp[i][j].rgbtBlue = (int) round((float) sumB / counter);
        }
    }

    // Copy the blurred result back into the original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
        }
    }

    return;
}
