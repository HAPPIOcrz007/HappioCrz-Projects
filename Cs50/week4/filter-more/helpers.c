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

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Sobel kernels matrices
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}}; // x axis done
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}}; // y axis done

    RGBTRIPLE tempo[height][width]; // temporary storage

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumRx = 0, sumRy = 0;
            int sumGx = 0, sumGy = 0;
            int sumBx = 0, sumBy = 0;

            // loop over the 3x3 grid like did in past ones
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    // treat out-of-bounds as black (0) the edge cases
                    if (ni < 0 || ni >= height || nj < 0 || nj >= width)
                        continue;

                    int weightX = Gx[di + 1][dj + 1];
                    int weightY = Gy[di + 1][dj + 1];

                    sumRx += image[ni][nj].rgbtRed * weightX;
                    sumRy += image[ni][nj].rgbtRed * weightY;

                    sumGx += image[ni][nj].rgbtGreen * weightX;
                    sumGy += image[ni][nj].rgbtGreen * weightY;

                    sumBx += image[ni][nj].rgbtBlue * weightX;
                    sumBy += image[ni][nj].rgbtBlue * weightY;
                }
            }
yes
            // compute magnitude for each channel
            int red = round(sqrt(sumRx * sumRx + sumRy * sumRy));
            int green = round(sqrt(sumGx * sumGx + sumGy * sumGy));
            int blue = round(sqrt(sumBx * sumBx + sumBy * sumBy));

            // cap values at 255
            red = fmin(red, 255);
            green = fmin(green, 255);
            blue = fmin(blue, 255);

            // threshold logic
            if (red < 10)
                red = 0;
            if (green < 10)
                green = 0;
            if (blue < 10)
                blue = 0;

            tempo[i][j].rgbtRed = red;
            tempo[i][j].rgbtGreen = green;
            tempo[i][j].rgbtBlue = blue;
        }
    }

    // copy back the values from tempo to image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = tempo[i][j];
        }
    }
    return;
}
// thanks to the previous questions it was easy to solve this one
// with only some research
