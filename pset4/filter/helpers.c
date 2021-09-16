#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Iterate through pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate the average of red, green and blue value for each pixel 
            float avg = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            
            // Filter pixels
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    
    // Iterate through pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Use formula for red
            float sepiaRed = round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue);
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            
            // Use formula for green
            float sepiaGreen = round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue);
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            
            // Use formula for Blue
            float sepiaBlue = round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue);
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            
            // Assign filtered colours into old ones
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Temporary variable
    RGBTRIPLE hold;

    // Iterate through pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // Reflect: swap pixels on the left with pixels on the right with the same distance to the middle pixel.
            hold = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = hold;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Temporary viarable
    RGBTRIPLE temp_image[height][width];
 
    // Iterate through pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int finalRed = 0;
            int finalGreen = 0;
            int finalBlue = 0;
            int counter = 0;

            // Go to neighbouring pixels
            for (int a = -1; a <= 1; a++)
            {
                for (int b = -1; b <= 1; b++)
                {
                    // If the i-value or j-value is invalid, ignore the pixel
                    if (i + a >= 0 && i + a <= height - 1 && j + b >= 0 && j + b <= width - 1)
                    {
                        finalRed = finalRed + image[i + a][j + b].rgbtRed;
                        finalGreen = finalGreen + image[i + a][j + b].rgbtGreen;
                        finalBlue = finalBlue + image[i + a][j + b].rgbtBlue;
                        counter++;
                    }
                }
            }
            temp_image[i][j].rgbtRed = (int) round((float) finalRed / (float) counter);
            temp_image[i][j].rgbtGreen = (int) round((float) finalGreen / (float) counter);
            temp_image[i][j].rgbtBlue = (int) round((float) finalBlue / (float) counter);
        }
    }
    
    // Assign blured pixels into old ones
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp_image[i][j];
        }
    }
    return;
}