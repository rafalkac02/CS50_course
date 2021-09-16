#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


// define byte
typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    // one user entry
    if (argc != 2)
    {
        printf("Usage: ./recover image \n");
        return 1;
    }

    // input file name
    char *file = argv[1];

    // open file
    FILE *inptr = fopen(file, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", file);
        return 4;
    }

    // scroll through and look for beginning of jpeg
    int x = 512;
    int cnt = 0;
    int jpg_start = 0;

    //create output file, initialize to null
    FILE *outptr = NULL;

    //create array of bytes
    BYTE buffer[x];

    // read into array of bytes from inptr
    while (fread(buffer, 512, 1, inptr) == 1)
    {
        // check for jpeg header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // write into new jpeg
            jpg_start = 1;

            // create string array for xxx.jpg file name: 7 chars plus null terminator = 8
            char filename[8];
            sprintf(filename, "%03i.jpg", cnt);

            // open file
            outptr = fopen(filename, "w");
            cnt++;
        }

        // after first jpeg header has been found
        if (jpg_start == 1)
        {
            // write to open file
            fwrite(&buffer, 512, 1, outptr);
        }
    }
    fclose(outptr);
    fclose(inptr);
    return 0;
}
