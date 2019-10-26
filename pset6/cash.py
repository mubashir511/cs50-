from cs50 import get_float

# Get dollar value from user
while True:
    cash = get_float("Change owed: ")
    if cash > 0:
        break

# Convert dollar value into cents
cents = cash * 100

# Declaring other variables
q25 = 0
q10 = 0
q5 = 0
q1 = 0

# Checking for quarters
if ((cents // 25) >= 1):
    q25 = cents // 25
    cents = cents % 25

# Checking for dimes
if ((cents // 10) >= 1):
    q10 = cents // 10
    cents = cents % 10

# Checking for nickels
if ((cents // 5) >= 1):
    q5 = cents // 5
    cents = cents % 5

# Checking for pennies
if ((cents // 1) >= 1):
    q1 = cents / 1

# Taking sum all the avaiable type of coins
coins = q25 + q10 + q5 + q1
print(f"coins: {coins}")