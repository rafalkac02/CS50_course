# Plagiarism Checker
#### Video Demo: https://youtu.be/lbHb5E4VzPg
#### Description:
Plagiarism Checker is a program that helps to detect possible plagiarism.

It is a perfect solution for a teacher who received multiple essays from pupils and wants to check if anyone has cheated. Using this program, the teacher can quickly examine if there are pairs of essays that highly resemble each other. The program shows a sorted list of pairs with similarity percentage rates. The authors with the highest similarity between their pieces of works are shown at the top, so the user can immediately know if anyone potentially copied their work.

To create it, I used several programming languages and frameworks, including Python, Flask, SQL, HTML, CSS.

Inside my project folder, I made separate folders called static and templates. Static folder is for CSS styling file, while templates are for HTML code for each route in my web application.

I created the following templates: layout.html for arranging constant design for all pages; register.html for registering; login.html for singing in; about.html for about page; changepassword.html for changing user's password; index.html for the homepage, where you begin the process of plagiarism checking; files.html is the second step, this template displays form to upload files, changing dynamically according to user's input on the homepage; similarities.html displays output of the whole plagiarism checking process; history.html shows a list of comparisons ever ran by the user and lets them retrieve the data from each one; finally the data.html shows that retrieved data after such request in history.html.

Yet, the whole functionality of the program is contained in python files - app.py supported by helpers.py, where some functions are defined. There is also plagiarism.db database which stores data such as a list of users and their history.

There were certain design choices I have made along the way. The most important and debated ones concerned the algorithm calculating the similarity between two text files since it is a prominent point of the application. I have decided to use the ratio() of SequenceMatcher function from difflib library since it returns a measure of the sequences’ similarity as a float in the range [0, 1], so it can be easily transferred to a percentage value. The function's formula is 2M/T where T is the total number of elements in both sequences, and M is the number of matches. It returns 1.0 for identical sequences and 0.0 if they have nothing in common.
According to official documentation: "The result of a ratio() call may depend on the order of the arguments. For instance:
```
>>> SequenceMatcher(None, 'tide', 'diet').ratio()
0.25
>>> SequenceMatcher(None, 'diet', 'tide').ratio()
0.5 "
```
To solve that problem, my program calculates both values and shows the higher to the user. I have also chosen to format the similarity rate as XX% (or X%), with no coma and tens of number since output quickly becomes messy.

Furthermore, I have decided not to exclude any white spaces from comparison. This is because space, tab and enter characters are all part of written work. Moreover, if someone, for instance, copied somebody's work and changed few words for synonyms, excluding white spaces would slightly lower the similarity score between these two. That's why I made every character equal in the comparison calculate function. During testing, the difference between these two settings turned out to be negligible.

Another decision I made was to make the user provide the author of each file when uploading. The output would be very hard to read because the program would identify pieces of work only by the filename. It would be extremely problematic if several files shared the same name, making it impossible to differentiate them. I have restricted author input to max of 40 characters because if it accepted any length, it could cause problems in the output table.