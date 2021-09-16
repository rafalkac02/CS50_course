from cs50 import get_int

# prompt for height between 1 and 8
height = 0
while not 1 <= height <= 8:
    height = get_int("Height: ")

# print as many rows as provided height
for i in range(height):

    # left-side spaces
    for j in range(height-i-1):
        print(" ", end="")

    # left-side hashes
    for j in range(i+1):
        print("#", end="")

    # separate pyramid's halves
    print("  ", end="")

    # right-side hashes
    for j in range(i+1):
        print("#", end="")

    # new row
    print()