from sys import argv, exit
from cs50 import SQL
from csv import DictReader

# Proper usage
if len(argv) != 2:
    print("Usage: python import.py example.csv")
    exit(1)

# Set up a database connection
db = SQL("sqlite:///students.db")

# Open the csv file
with open(argv[1], "r") as inputfile:
    reader = DictReader(inputfile)
    
    # Iterate over csv file
    for row in reader:
        name = row["name"].split(" ")
        house = row["house"]
        birth = row["birth"]
        
        # If person has middle name
        if len(name) == 3:
            first_n = name[0]
            middle_n = name[1]
            last_n = name[2]
            
        # If person has no middle name
        elif len(name) == 2:
            first_n = name[0]
            middle_n = None
            last_n = name[1]
            
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?,?,?,?,?)", 
                   first_n, middle_n, last_n, house, birth)