from cs50 import get_string
import sys

# Finding correct key
digit = 0
argc = len(sys.argv)

if (argc == 2):

    # Get key argument
    key = sys.argv[1]

    # Check if key is a number
    if (key.isdigit() == False):
        print("Usage: ./caesar key")
        sys.exit(1)
    else:
        # Convert key into an integer
        key = int(sys.argv[1])

        # Asking Plain text
        p_tx = get_string("plaintext: ")

        # Declaring ciphertext string
        cx_tx = []

        # length of plain text
        txt_len = len(p_tx)

        # Shifting letters in the string
        for j in range(txt_len):

            # Shifting lowercase alphabets
            if ((p_tx[j] >= 'a') and (p_tx[j] <= 'z')):
                count = ord(p_tx[j])
                chk_count = (count - 1)
                ans = count + key

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
                chk_count = (count - 1)
                ans = count + key

                while(count <= ans):
                    if (chk_count == 90):
                        chk_count = 65
                        count += 1
                    else:
                        chk_count += 1
                        count += 1

                cx_tx.append(chr(chk_count))

            else:
                cx_tx.append(p_tx[j])

        print("ciphertext: ", end="")
        for i in cx_tx:
            print(i, end="")
        print()

else:
    print("Usage: ./caesar key")
    sys.exit(1)
