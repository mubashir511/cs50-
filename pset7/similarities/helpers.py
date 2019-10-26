from nltk.tokenize import sent_tokenize

# Function to find similarity between two lists


def similarities(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    # Remove dublicates
    return list(dict.fromkeys(lst3))


def lines(a, b):
    """Return lines in both a and b"""

    # make list of lines in file 'a'
    list_a = a.split('\n')
    # make list of lines in file 'b'
    list_b = b.split('\n')

    result = similarities(list_a, list_b)
    return result


def sentences(a, b):
    """Return sentences in both a and b"""

    list_a = sent_tokenize(a)
    list_b = sent_tokenize(b)

    result = similarities(list_a, list_b)
    return result


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    def splitSubstring(lst, n):
        substring = []
        length = len(lst)

        for i in range(length - n + 1):
            substring.append(lst[i:i+n])

        return substring

    # find substrings for string 'a'
    list_a = splitSubstring(a, n)
    # find substrings for string 'b'
    list_b = splitSubstring(b, n)

    result = similarities(list_a, list_b)
    return result
