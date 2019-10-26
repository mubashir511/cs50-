from crypt import crypt
import sys

# hash value of passaward
hash_old = "abBZmQBTazHcs"

argc = len(sys.argv)

# Check if argument is pesent
if (argc == 2):

    # Getting input string
    c = len(sys.argv[1])

    # If only one argument is present
    if ((argc == 2) and (c <= 5)):

        # Getting input password = mubi
        s = sys.argv[1]

        for i in range(c):
            # Checking for numeric digits
            if (s[i].isalpha() == 0):
                print("your passward is incorrect")
                sys.exit(1)

    else:
        print("Usage: python crack.py passaword")
        sys.exit(1)

    # Computing hash value of the give valu
    hash_new = crypt(s, "ab")

    # Comparing both hashes
    if (hash_old == hash_new):
        print(f"passward: {s}")
        sys.exit(1)
    else:
        print("your passward is incorrect")
        sys.exit(1)
else:
    print("Usage: python crack.py passaword")
    sys.exit(1)