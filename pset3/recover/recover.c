#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: copy infile outfile\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[1];

    // open input file
    FILE *inptr = fopen(infile, "r");

    // Does the input file exist or readable? If not fail-over.
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 1;
    }
    // Allocating space for buffer
    unsigned char buffer[512];

    // Tracking variables
    long byte_count = 1;
    int jpeg_count = 0;
    int file_open = 0;

    // Initialize file name and img_file
    char filename[10];
    FILE *img_file;

    // Read block from file
    while (fread(&buffer, 512, 1, inptr))
    {
        // Start of a jpeg file
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If a jpeg file is already open
            if (file_open)
            {
                // close the previously opened file
                fclose(img_file);
                // Identifer that file closed now
                file_open = 0;

                // create new file name
                sprintf(filename, "%03d.jpg", jpeg_count);

                // apply and open this new file
                img_file = fopen(filename, "a");

                // set openFileTracker to true
                file_open = 1;

                // Increment our file naming tracker
                jpeg_count++;
            }
            if (!file_open)
            {
                // create new file name
                sprintf(filename, "%03d.jpg", jpeg_count);

                // apply and open this new file
                img_file = fopen(filename, "w");

                // set openFileTracker to true
                file_open = 1;

                // Increment our file naming tracker
                jpeg_count++;
            }
            // write the buffer to the file
            fwrite(&buffer, 512, 1, img_file);
        }
        else
        {
            // Not the star of jpeg file
            if (file_open)
            {
                // Write the block to the file
                fwrite(&buffer, 512, 1, img_file);
            }
        }
        byte_count++;
    }

    printf("total bytes = %li\n", byte_count);
    printf("jgeg# %i\n", jpeg_count);

    // While loop terminated:  we have reached EOF
    // Close the initial image file
    fclose(inptr);

    // close any open jpeg file
    fclose(img_file);

    return 0;

}
