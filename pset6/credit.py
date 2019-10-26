from cs50 import get_int

# Gets number from user
num = None
while True:
    num = get_int("Number: ")
    if num > 0:
        break

# Apply Luhn's Algorithum
m = n = temp = None
key = 0
Sum = 0
sw = 0
sm = 0
while True:

    # Finding the first digit of the number
    if (num // 10) < 1:
        n = num

    # Split long number into digits
    # Taking mod of number
    m = num % 10

    # separating alternate digits
    if (key == 0):
        # Sum of the digits that weren’t multiplied by 2
        sw = sw + m
        key = 1
    else:
        # Multiply every other digit by 2
        # Starting with the number’s second-to-last digit
        m *= 2
        if (m < 10):
            sm = sm + m
        else:
            while True:
                temp = m % 10
                m = m // 10
                sm = temp + m + sm
                if (m // 10) < 1:
                    break
        key = 0

    # Decrease the length of card number by one digit
    num = num // 10

    if num <= 0:
        break

# Finding sum
Sum = sw + sm

# Select the write card
if ((Sum % 10) == 0):
    if (n == 3):
        print("AMEX")
    elif (n == 5):
        print("MASTERCARD")
    elif (n == 4):
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")

