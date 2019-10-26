# Importing get_string function from cs50 library
from cs50 import get_string
# Getting name from the user
name = get_string("What is your name? ")
# Print the given name
print(f"hello, {name}")