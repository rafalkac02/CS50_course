from cs50 import SQL
from datetime import datetime
from difflib import SequenceMatcher
from flask import Flask, render_template, request, abort, url_for, redirect, session, flash
from operator import itemgetter
from pytz import timezone
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import RegistrationForm, LoginForm, text_file, login_required, password_duplicate, RequestResetForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "8pdRPAdU78"

db = SQL("sqlite:///plagiarism.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    return render_template("index.html")


@app.route("/about")
@login_required
def about():

    return render_template("about.html")


@app.route("/register", methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirm_password")
        hash = generate_password_hash(password)

        hashes = db.execute("SELECT hash FROM users")

        # Ensure username, email and password are available
        if db.execute("SELECT * FROM users WHERE username = ?", username):
            flash("Username already taken", "danger")

        elif db.execute("SELECT * FROM users WHERE email = ?", email):
            flash("Email already taken", "danger")

        elif password_duplicate(hashes, password):
            flash("Password already taken", "danger")

        # Correct input
        else:

            # Update database
            db.execute("INSERT INTO users (username, email, hash) VALUES(?, ?, ?)", username, email, hash)

            # Remember which user has logged in
            session["user_id"] = db.execute("SELECT * FROM users WHERE username = ?", username)[0]["id"]

            flash(f'{username} has been successfully registered!', 'success')
            return redirect("/")

    return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        email = request.form.get("email")
        password = request.form.get("password")

        # Query database for email
        row = db.execute("SELECT * FROM users WHERE email = ?", email)

        # Correct data
        if row and check_password_hash(row[0]["hash"], password):
            # Remember which user has logged in
            session["user_id"] = row[0]["id"]
            return redirect("/")

        # Invalid data
        else:
            flash("Invalid email and/or password.", "danger")

    return render_template("login.html", form=form)


@app.route("/files", methods=["GET", "POST"])
def files():

    if request.method == "POST":

        n = session["n"]
        user_id = session["user_id"]

        # Populate list of files with dictionaries to store each file's name, author and content
        files=[]
        for i in range(n):
            files.append({})
            file = request.files[f"file{i}"]

            # error checking:
            if not text_file(file.filename):
                flash("Please provide text files!", "danger")
                return redirect(f"/files?n={n}")

            files[i]["filename"] = file.filename
            files[i]["author"] = request.form.get(f"author{i}")
            files[i]["text"] = file.read().decode("utf-8")


        # Populate list of pairs with all possible pairs; x - counter
        pairs=[]
        x = 0

        # files[i] makes a pair with files[j]
        for i in range(0, n-1):

            for j in range(i+1, n):
                pairs.append({})

                pairs[x]["filename_1"] = files[i]["filename"]
                pairs[x]["author_1"] = files[i]["author"]

                pairs[x]["filename_2"] = files[j]["filename"]
                pairs[x]["author_2"] = files[j]["author"]

                # Calculate pair's similarity
                #   Difflib library documentation: "The result of a ratio() call may depend on the order of the arguments."
                #   Thus, let's calculate both and use higher value. Also, let's ignore any space charachters in comparision
                s1 = SequenceMatcher(None, files[i]["text"], files[j]["text"]).ratio()
                s2 = SequenceMatcher(None, files[j]["text"], files[i]["text"]).ratio()

                if s1 > s2:
                    pairs[x]["similarity"] = int(round(s1, 2) * 100)
                else:
                    pairs[x]["similarity"] = int(round(s2, 2) * 100)

                # This solution prevents strange output like 28.000000000000004%, which occured during testing
                #pairs[x]["similarity"] = pairs[x]["similarity"].split(".", 1)[0] + "%"

                x += 1

        # Sort pairs by similarity in descending order
        sorted_pairs = sorted(pairs, key=itemgetter("similarity"), reverse=True)

        for pair in sorted_pairs:
            pair['similarity'] = f"{pair['similarity']}%"

        # Update the history table in the database
        fmt = "%d.%m.%Y %H:%M"
        now = datetime.now(timezone("Europe/Warsaw")).strftime(fmt)
        db.execute("INSERT INTO history (user_id, datetime, n, similarity) VALUES(?, ?, ?, ?)", user_id, now, n, sorted_pairs[0]["similarity"])

        # Copy similarities.html table into database so it can be retrieved later
        for pair in sorted_pairs:
            db.execute("INSERT INTO tables (user_id, datetime, author_1, author_2, similarity) VALUES(?, ?, ?, ?, ?)",
                        user_id, now, f"{pair['author_1']} ({pair['filename_1']})", f"{pair['author_2']} ({pair['filename_2']})", pair['similarity'])

        return render_template("similarities.html", sorted_pairs=sorted_pairs)


    # GET method
    else:
        # Error checking
        if not request.args.get("n"):
            flash("Please select at least 2 so we can compare files!", "danger")
            return redirect("/")

        n = int(request.args.get("n"))
        session["n"] = n

        if n < 2:
            flash("Please select at least 2 so we can compare files!", "danger")
            return redirect("/")

        return render_template("files.html", n=range(n))


@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def changepassword():
    if request.method == "POST":
        user_id = session["user_id"]
        row = db.execute("SELECT * FROM users WHERE id = :id", id=user_id)
        password = request.form.get("pass")
        new_pass_1 = request.form.get("new_pass_1")
        new_pass_2 = request.form.get("new_pass_2")

        # Check the old password
        if not check_password_hash(row[0]["hash"], password):
            flash("Old password is invalid.", "danger")

        # Check new passwords
        elif new_pass_1 != new_pass_2:
            flash("New passwords do not match", "danger")

        # Check for a duplicate
        elif password == new_pass_1:
            flash("The new password must differ from the current one.", "danger")

        else:

            # Update user's password
            db.execute("UPDATE users SET hash = :hash WHERE id = :id",
                       hash=generate_password_hash(new_pass_1), id=user_id)

            flash("Password successfully updated.", "success")
            return redirect("/")

        return redirect("/change_password")

    else:
        return render_template("changepassword.html")


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():

    rows = db.execute("SELECT * FROM history WHERE user_id = :user_id ORDER by datetime DESC", user_id=session["user_id"])
    return render_template ("history.html", rows=rows)


@app.route("/data", methods=["GET", "POST"])
@login_required
def data():
    if request.method == "POST":

        datetime = request.form.get("datetime")

        pairs = db.execute("SELECT author_1, author_2, similarity FROM tables WHERE user_id = :user_id AND datetime = :datetime", user_id=session["user_id"], datetime=datetime)

        return render_template ("data.html", datetime=datetime, pairs=pairs)

    else:
        return redirect("/history")