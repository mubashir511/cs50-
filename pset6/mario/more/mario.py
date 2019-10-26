# Import get_int func from cs50 library
from cs50 import get_int
# Get user input
while True:
    height = get_int("Height: ")
    if height > 0 and height <= 8:
        break
# Print pyramind
for i in range(height):
    # Print left pyramind
    for j in range(height):
        if j < ((height - i) - 1):
            print(" ", end="")
        else:
            print("#", end="")
    print("  ", end="")
    # Print right pyramind
    for k in range(i + 1):
        print("#", end="")
    print("")
