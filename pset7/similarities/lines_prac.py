
import sys

# Function to find similarity between two lists
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    # Remove dublicates
    return list(dict.fromkeys(lst3))

def lines(a,b):

    # open file 'a'
    with open(a) as file:
        # make list of lines in file 'a'
        list_a = [line.rstrip('\n') for line in file]

    # open file 'b'
    with open(b) as file:
        # make list of lines in file 'a'
        list_b = [line.rstrip('\n') for line in file]

    result = intersection(list_a, list_b)

    for x in result:
        print(x)

file1 = sys.argv[1]
file2 = sys.argv[2]
lines(file1, file2)
