from sys import argv, exit
from cs50 import SQL
from csv import DictReader

# Proper usage
if len(argv) != 2:
    print("Usage: python roster.py house_name")
    exit(1)

# Set up a database connection
db = SQL("sqlite:///students.db")

# Return a list of specified house residents
residents = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", argv[1])

# Print people from residents' list
for row in residents:
    if row["middle"] == None:
        print(f"{row['first']} {row['last']}, born {row['birth']}")
    else:
        print(f"{row['first']} {row['middle']} {row['last']}, born {row['birth']}")