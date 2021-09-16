from cs50 import get_int
import sys

# get positive integer
number = 0
while number <= 0:
    number = get_int("Number: ")

s_number = str(number)
length = len(s_number)

# check for valid length
lengths = [13, 15, 16]
if length not in lengths:
    print("INVALID")
    sys.exit(1)

# Luhn's algorithm
total = 0

# add every other digit, starting with number's last digit
for c in range(length - 1, -1, -2):
    total += int(s_number[c])

# multiply every other digit by 2, starting with the number’s second-to-last digit
# then, add every digit of the results
for c in range(length - 2, -1, -2):
    x = 2 * int(s_number[c])
    for i in str(x):
        total += int(i)

# check for Luhn's algorithm correctness
if total % 10 != 0:
    print("INVALID")
    sys.exit(1)

# find out the company
mastercard = "51", "52", "53", "54", "55"
amex = "34", "37"
visa = "4"

if s_number[:2] in mastercard and length == 16:
    print("MASTERCARD")
elif s_number[:2] in amex and length == 15:
    print("AMEX")
elif s_number[:1] in visa and length in [13, 16]:
    print("VISA")
else:
    print("INVALID")
    sys.exit(1)