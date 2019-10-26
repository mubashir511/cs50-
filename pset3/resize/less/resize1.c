#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    float n = atof(argv[1]);

    if (n == 0)
    {
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }

    else if ((argc != 4) || (n / trunc(n)) != 1 || (n < 1) || (n > 100))
    {
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    FILE *outptread = fopen(outfile, "r");
    if (outptr == NULL || outptread == NULL)
    {
        fclose(inptr);
        printf("Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        printf("Unsupported file format.\n");
        return 4;
    }

    int Factor = n;

    // determine padding for scanlines in original file
    int OriginalPadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // determine padding for scanlines in new file
    int NewPadding = (4 - (bi.biWidth * Factor * sizeof(RGBTRIPLE)) % 4) % 4;

    // store original width and height
    int OriginalWidth = abs(bi.biWidth);
    int OriginalHeight = abs(bi.biHeight);

    // delete afterwards
    printf("Factor: %i\nWidth: %i\nHeight: %i\n", Factor, bi.biWidth, bi.biHeight);
    printf("bfSize: %i\nbfoffbits: %i\nbisizeimage: %i\nOriginalPadding; %i\nNewpadding: %i\n", bf.bfSize, bf.bfOffBits, bi.biSizeImage, OriginalPadding, NewPadding);
    printf("\n");

    // change key information BITMAPFILEHEADER and BITMAPFILEHEADER due to resizing
    bi.biWidth = bi.biWidth * Factor;
    bi.biHeight = bi.biHeight * Factor;
    bf.bfSize = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) + abs(bi.biWidth) * abs(bi.biHeight) * sizeof(RGBTRIPLE) + NewPadding * abs(bi.biHeight) * sizeof(BYTE);
    bi.biSizeImage = bf.bfSize - bf.bfOffBits;

    // delete afterwards
    printf("Factor: %i\nWidth: %i\nHeight: %i\n", Factor, bi.biWidth, bi.biHeight);
    printf("bfSize: %i\nbfoffbits: %i\nbisizeimage: %i\nOriginalPadding; %i\nNewpadding: %i\n", bf.bfSize, bf.bfOffBits, bi.biSizeImage, OriginalPadding, NewPadding);

    // create temp variable to store each scanline in outputfile
    int ScanlineBytes = sizeof(RGBTRIPLE) * bi.biWidth + sizeof(BYTE) * NewPadding;
    BYTE* Scanline = malloc(sizeof(BYTE) * ScanlineBytes);

    printf("Size of Scanline in Bytes: %i\n", ScanlineBytes); // delete afterwards

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0; i < OriginalHeight; i++)
    {
        // iterate over pixels in scanline
        for (int j = 0; j < OriginalWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // write RGB triple to outfile Factor times
            for (int k = 0; k < Factor; k++)
            {
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }

        }

        // skip over padding, if any
        fseek(inptr, OriginalPadding, SEEK_CUR);

        // then add it back (to demonstrate how)
        for (int l = 0; l < NewPadding; l++)
        {
            fputc(0x00, outptr);
        }

        // write (Factor - 1) additional scanlines for new height
        fseek(outptread, -1 * ScanlineBytes, SEEK_END);
        fread(&Scanline, ScanlineBytes, 1, outptread);
        for (int z = 0; z < (Factor - 1); z++)
            {
                fwrite(&Scanline, ScanlineBytes, 1, outptr);
            }

    }

    // close infile
    fclose(inptr);

    // close outfiles
    fclose(outptr);
    fclose(outptread);

    // free Scanline
    free(Scanline);

    // success
    return 0;
}