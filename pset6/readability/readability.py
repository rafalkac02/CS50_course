from cs50 import get_string

# prompt for input
text = get_string("Text: ")

words = len(text.split())
letters = 0
sentences = 0

# calculate letters and sentences
for c in text:
    if c.isalpha():
        letters += 1
    if c == "." or c == "!" or c == "?":
        sentences += 1

# calculate index
L = 100 * letters/words     # average number of letters per 100 words
S = 100 * sentences/words   # average number of sentences per 100 words in the text

index = 0.0588 * L - 0.296 * S - 15.8

# output the index
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {round(index)}")