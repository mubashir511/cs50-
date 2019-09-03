// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: copy infile outfile\n");
        return 1;
    }

    // Accepting 'resize' value
    float resize_val = atof(argv[1]);
    // Checking if 'n' is between 0-100
    if (resize_val >= 0 && resize_val <= 100)
    {
        printf("n = %f\n", resize_val);
    }
    else
    {
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    // Does the input file exist or readable? If not fail-over.
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    // Does the output file now exist or writable? If not fail-over
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
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
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }


    // determine padding for scanlines
    float old_padding = fmod((4 - fmod((bi.biWidth * sizeof(RGBTRIPLE)), 4)), 4);
    printf("old-padding: %f\n", old_padding);

    // Determing new padding for scanlines
    float new_padding = fmod((4 - fmod((bi.biWidth * sizeof(RGBTRIPLE) * resize_val), 4)), 4);
    printf("new-padding: %f\n", new_padding);

    // Note old width and height of image
    int old_w = abs(bi.biWidth);
    int old_h = abs(bi.biHeight);

    // Calculate new width and height of image
    int new_w = old_w * resize_val;
    int new_h = old_h * resize_val;

    bi.biWidth = new_w;
    bi.biHeight = new_h * (-1);

    // change key information BITMAPFILEHEADER and BITMAPFILEHEADER due to resizing
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * new_w) + new_padding) * new_h;
    bf.bfSize = (sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) + bi.biSizeImage);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);


    printf("w-old: %i pixels , w-new: %i pixels \n", old_w, new_w);
    printf("h-old: %i pixels, h-new: %i pixels\n", old_h, new_h);
    printf("ImageSize(pixels, padding): %i bytes\n", bi.biSizeImage);
    printf("sizeRGB: %lu\n", sizeof(RGBTRIPLE));
    printf("Filesize(pixels, padding and header): %i bytes\n", bf.bfSize);

    // If size is increasing
    if (new_w >= old_w && new_h >= old_w)
    {
        // Allocating memory for each scanline
        RGBTRIPLE *scanline = malloc(old_w * 3);
        // temporary storage
        RGBTRIPLE triple;

        for (int i = 0; i < old_h; i++)
        {
            // Resize horizontally
            for (int j = 0 ; j < old_w; j++)
            {
                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
                scanline[j] = triple;

                // write RGB triple to outfile
                for (int k = 0; k < resize_val; k++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }
            // Applying padding
            if (new_padding != 0)
            {
                for (int pad = 0; pad < new_padding; pad++)
                {
                    fputc(0x00, outptr);
                }
            }

            // Resize vertically
            // For every new row appended
            for (int k = 0; k < (resize_val - 1); k++)
            {
                // For every pixel in the row
                for (int l = 0; l < old_w; l++)
                {
                    // Increase every pixel by nth (resize_val) times
                    for (int m = 0; m < resize_val; m++)
                    {
                        // write RGB triple to outfile
                        fwrite(&scanline[l], sizeof(RGBTRIPLE), 1, outptr);
                    }
                }
                // Applying padding
                if (new_padding != 0)
                {
                    for (int pad = 0; pad < new_padding; pad++)
                    {
                        fputc(0x00, outptr);
                    }
                }
            }
            // skip over padding, if any
            fseek(inptr, old_padding, SEEK_CUR);
        }
        // free space
        free(scanline);
    }
    else
    {
        int drop = (old_w / new_w);
        printf("drop: %i\n\n", drop);
        // Allocating memory for each scanline
        RGBTRIPLE *scanline = malloc(new_w * 3);
        // temporary storage
        RGBTRIPLE triple;
        // Moving vertically
        for (int i = 0; i < old_w; i += drop)
        {
            // Moving horizontally
            // Read pixels from infile
            for (int j = 0; j < new_w; j++)
            {
                // Read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
                scanline[j] = triple;
                // Skiping extra pixels
                if (j < new_w - 1)
                {
                    fseek(inptr, 3, SEEK_CUR);
                }
                // skiping extra pixels and padding
                else
                {
                    fseek(inptr, 3 + old_padding, SEEK_CUR);
                }
            }
            // Skiping extra rows
            fseek(inptr, (old_w * 3) + (int) old_padding, SEEK_CUR);

            // Writing pixels
            for (int k = 0; k < new_w; k++)
            {
                // write RGB triple to outfile
                fwrite(&scanline[k], sizeof(RGBTRIPLE), 1, outptr);
            }
            // Applying padding
            if (new_padding != 0)
            {
                for (int pad = 0; pad < new_padding; pad++)
                {
                    fputc(0x00, outptr);
                }
            }


        }
        // free space
        free(scanline);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
