from cs50 import get_string
from sys import argv
import sys


def main():

    # Find if argument is present
    argc = len(sys.argv)
    if (argc == 2):

        # Take file name
        filename = sys.argv[1]

        # Store each word in file into a list
        file_word = []

        with open(filename) as file:
            file_word = [line.rstrip('\n') for line in file]

        file_len = len(file_word)

        # Take input from the user for censoring
        token = get_string("What message would you like to censor?\n")

        # Store each word in file into a list
        token_word = []

        token_word = token.split()
        token_len = len(token_word)

        # Applying censoring
        # iterate over each token word
        for i in range(token_len):

            # check if token is present in the file
            if (token_word[i] in file_word) or (token_word[i].lower() in file_word) or (token_word[i].upper() in file_word):

                # Get length of word
                star_len = len(token_word[i])

                # Print star in place of the word
                for j in range(star_len):
                    print("*", end="")
                    #print(f"Yes, element '{token_word[i]}' found in List")
            else:
                print(token_word[i], end="")

            # Print space between words
            print(" ", end="")

        print()

    else:
        print("Usage: python bleep.py dictionary")
        sys.exit(1)


if __name__ == "__main__":
    main()
