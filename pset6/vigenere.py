from cs50 import get_string
import sys

# Check if argument value is present
if (sys.argv[1] == None):
    print("Usage: python vigenere.py k")
    sys.exit(1)

# Finding correct key
digit = 0
argc = len(sys.argv)

# check if only one argument is present
if (argc == 2):

    # Get key argument
    key_str = sys.argv[1]
    key_len = len(key_str)

    # Check if argument is alphabets
    if (key_str.isalpha() == False):
        print("Usage: python vigenere.py k")
        sys.exit(1)
    else:

        # make an array that will contain ascii values of the characters in the key values
        key = []

        # array for ciphertext
        cx_tx = []

        for c in key_str:
            if ((c >= 'a') and (c <= 'z')):
                key.append(ord(c) - 97)

            elif ((c >= 'A') and (c <= 'Z')):
                key.append(ord(c) - 65)

            else:
                print("invalid keyword")
                sys.exit(1)

    # Applying encryption
    # Asking Plain text
    p_tx = get_string("plaintext: ")
    p_len = len(p_tx)

    key_index = 0

    # Shifting letters in the string
    for j in range(p_len):

        # Shifting lowercase alphabets
        if ((p_tx[j] >= 'a') and (p_tx[j] <= 'z')):
            count = ord(p_tx[j])
            chk_count = count - 1
            ans = count + key[key_index]

            while(count <= ans):
                if (chk_count == 122):
                    chk_count = 97
                    count += 1
                else:
                    chk_count += 1
                    count += 1

            cx_tx.append(chr(chk_count))

        # Shifting uppercase alphabets
        elif ((p_tx[j] >= 'A') and (p_tx[j] <= 'Z')):
            count = ord(p_tx[j])
            chk_count = count - 1
            ans = count + key[key_index]

            while(count <= ans):
                if (chk_count == 90):
                    chk_count = 65
                    count += 1
                else:
                    chk_count += 1
                    count += 1

            cx_tx.append(chr(chk_count))

        # Ignore empty spaces
        else:
            cx_tx.append(p_tx[j])
            key_index -= 1

        # Changing key array index
        if (key_index == (key_len - 1)):
            key_index = 0
        else:
            key_index += 1

    # printing cipheretext
    print("ciphertext: ", end="")
    for i in cx_tx:
        print(i, end="")
    print()

else:
    print("Usage: python vigenere.py k")
    sys.exit(1)

