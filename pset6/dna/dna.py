from sys import argv, exit
import itertools
import csv
import re

# Proper usage
if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)
    
# Read csv file as a list
with open(argv[1], "r") as inputfile:
    reader = list(csv.reader(inputfile))
    reader[0].remove("name")
    i = reader[0]   # i is a segement of DNA which contains wanted data from CSV file.
    
# Open sequence file
with open(argv[2], "r") as sequence:
    data = sequence.read()

# for each sequence
values_list = []
for n in range(len(i)):   # Iterate through each nucleotide
    counter = 0
    max_counter = 0
    location = 0
    previous_loc = 0
    
    # Do the following until dna sequence fully scanned
    while location < len(data):
        # Get the location where sequence is found
        location = data.find(i[n], location)
        if location == -1:   # If not found, reset the counter and break
            counter = 0
            break
        
        # If sequence occurs at the start of the sequence
        elif (location != -1) and previous_loc == 0:
            counter += 1
            max_counter = counter
            previous_loc = location
            
        # Sequence
        elif (location != -1) and ((location - len(i[n])) == previous_loc):
            counter += 1
            previous_loc = location
            if max_counter < counter:
                max_counter = counter
                
        # First found not at the start
        elif (location != -1) and ((location - len(i[n])) != previous_loc):
            counter = 1
            previous_loc = location
            if max_counter < counter:
                max_counter = counter
                
        location += 1
        
    # Get the largest number of sequencial occurances
    values_list.append(max_counter)

# Update the list to a list of strings to enable comparison
values_list = list(map(str, values_list))

# Make a new list to preserve reader
newlist = list(reader)
newlist.pop(0)

# Compare values_list to reader and if found, print the name of the person whos DNA matches
for person in newlist:
    if person[1:] == values_list:
        print(f"{person[0]}")
        break
    elif person == newlist[-1]:
        print("No match")
        