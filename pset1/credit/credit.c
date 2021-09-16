#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    // prompt for imput
    long N = get_long("Number: ");

    // 13-digit number
    if (N >= pow(10, 12) && N < pow(10, 13))
    {
        // calculate checksum
        int sum = 0;

        for (int i = 1; i < 12; i += 2)
        {
            int x = 2 * (N / (long)pow(10, i) % 10);
            if (x < 10)
            {
                sum += x;
            }
            else
            {
                sum += x / 10;
                sum += x % 10;
            }
        }

        for (int i = 0; i < 13; i += 2)
        {
            sum += N / (long)(pow(10, i)) % 10;
        }

        if (sum % 10 == 0 && N / (long)pow(10, 12) == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }

    // 15-digit number
    else if (N >= (long)pow(10,  14) && N < (long)pow(10, 15))
    {
        // calculate checksum
        int sum = 0;

        for (int i = 1; i < 14; i += 2)
        {
            int x = 2 * (N / (long)pow(10, i) % 10);
            if (x < 10)
            {
                sum += x;
            }
            else
            {
                sum += x / 10;
                sum += x % 10;
            }
        }

        for (int i = 0; i < 15; i += 2)
        {
            sum += N / (long)pow(10, i) % 10;
        }

        int first_two = N / (long)pow(10, 13);

        if (sum % 10 == 0 && (first_two == 34 || first_two == 37))
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }

    // 16-digit number
    else if (N >= (long)pow(10, 15) && N < (long)pow(10, 16))
    {
        // calculate checksum
        int sum = 0;

        for (int i = 1; i < 16; i += 2)
        {
            int x = 2 * (N / (long)pow(10, i) % 10);
            if (x < 10)
            {
                sum += x;
            }
            else
            {
                sum += x / 10;
                sum += x % 10;
            }
        }

        for (int i = 0; i < 15; i += 2)
        {
            sum += N / (long)pow(10, i) % 10;
        }

        int first_two = N / pow(10, 14);

        if (sum % 10 == 0 && N / (long)pow(10, 15) == 4)
        {
            printf("VISA\n");
        }
        else if (sum % 10 == 0 && (first_two == 51 || first_two == 52 || first_two == 53 || first_two == 54 || first_two == 55))
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}