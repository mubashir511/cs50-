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
    typedef unsigned char BYTE;
    BYTE *buffer = malloc (512);

    // Read block from file
    do
    {
        fread(buffer, 1, 512 ,inptr);
        printf("X ");
    }
    while (fread(&buffer, 512, 1 ,inptr) == 512);
    // Free the buffer space
    free(buffer);
}
