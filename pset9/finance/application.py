import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    owned = db.execute("SELECT * FROM wallet WHERE user_id = :user_id", user_id=session["user_id"])
    total = 0
    for stock in owned:
        stock["name"] = lookup(stock["symbol"])["name"]
        stock["price"] = lookup(stock["symbol"])["price"]
        stock["total"] = usd(float(stock["price"]) * int(stock["shares"]))
        total += float(stock["price"]) * int(stock["shares"])
    cash = float(db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])[0]["cash"])
    total += cash
    return render_template('index.html', owned=owned, cash=usd(cash), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        user_id = session["user_id"]
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # Error checking
        if not lookup(symbol) or not shares:
            return apology("invalid symbol and/or shares", 400)
        elif not shares.isdigit() or int(shares) < 1:
            return apology("shares must be positive integer", 400)

        # Check if user can afford the number of shares at the current price
        user_cash = float(db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)[0]["cash"])
        price = lookup(symbol)["price"]
        shares = int(shares)
        cost = float(price * shares)

        if cost > user_cash:
            return apology("You can't afford it", 400)

        # Record transaction
        db.execute("INSERT INTO transactions (user_id, type, symbol, shares, price) VALUES(?, ?, ?, ?, ?)",
                   user_id, "bought", symbol, shares, usd(price))

        # Update user's balance
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=user_cash-cost, user_id=user_id)

        # Update user's wallet
        owned = db.execute("SELECT * FROM wallet WHERE user_id = :user_id AND symbol = :symbol AND shares > 0",
                           user_id=user_id, symbol=symbol)
        if owned:
            db.execute("UPDATE wallet SET shares=(shares + :shares) WHERE user_id=:user_id AND symbol=:symbol",
                       shares=shares, user_id=user_id, symbol=symbol)
        else:
            db.execute("INSERT INTO wallet (user_id, symbol, shares) VALUES (:user_id, :symbol, :shares)",
                       user_id=user_id, symbol=symbol, shares=shares)

        # Successful transacion
        flash("Bought successfully.")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])

    for transaction in transactions:
        transaction["symbol"] = transaction["symbol"].upper()

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if not stock:
            return apology("Invalid symbol", 400)
        else:
            stock["price"] = usd(stock["price"])
            return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(password)

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not confirmation:
            return apology("must confirm password", 400)

        # Ensure passwords match
        elif password != confirmation:
            return apology("passwords don't match", 400)

        # Personal touch - require password to have at least one uppercase letter and at least one number
        elif not any(c.isupper() for c in password):
            return apology("password must contain at least one uppercase letter and at least one number", 400)
        elif not any(c.isdigit() for c in password):
            return apology("password must contain at least one uppercase letter and at least one number", 400)

        # Ensure username and password is available
        elif len(db.execute("SELECT * FROM users WHERE username = ?", username)) + len(db.execute("SELECT * FROM users WHERE hash = ?", hash)) > 0:
            return apology("invalid username and/or password")

        # Update database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Remember which user has logged in
        session["user_id"] = db.execute("SELECT * FROM users WHERE username = ?", username)[0]["id"]

        # Registered successfully
        flash("You have been successfully registered and logged in.")

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # Check for correct input
        try:
            shares = int(shares)
            if shares < 1:
                return apology("shares must be a positive integer", 400)
        except ValueError:
            return apology("shares must be a positive integer", 400)
        if not lookup(symbol):
            return apology("invalid symbol", 400)

        max_shares = db.execute("SELECT * FROM wallet WHERE user_id = ? AND symbol = ?", user_id, symbol)[0]["shares"]

        # Check for correct number of shares and update wallet
        if int(shares) > int(max_shares):
            return apology("too many shares", 400)
        elif int(shares) == int(max_shares):
            db.execute("DELETE FROM wallet WHERE user_id = ? AND symbol = ?", user_id, symbol)
        else:
            db.execute("UPDATE wallet SET shares= shares - ? WHERE user_id = ? AND symbol = ? ", shares, user_id, symbol)

        price = lookup(symbol)["price"]
        total = price * shares

        # Record transaction
        db.execute("INSERT INTO transactions (user_id, type, symbol, shares, price) VALUES (?, ?, ?, ?, ?)",
                   user_id, "sold", symbol.upper(), shares, price)

        # Update user's cash
        db.execute("UPDATE users SET cash=(cash + :total) WHERE id = :user_id", total=total, user_id=user_id)

        flash("Sold successfully.")
        return redirect("/")

    else:
        owned = db.execute("SELECT * FROM wallet WHERE user_id = :user_id", user_id=user_id)
        return render_template("sell.html", owned=owned)


# Personal touch - allow user to change password
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def changepassword():

    if request.method == "POST":
        user_id = session["user_id"]
        rows = db.execute("SELECT * FROM users WHERE id = :id", id=user_id)
        password = request.form.get("pass")
        new_pass = request.form.get("new1")

        # Check the old password
        if not check_password_hash(rows[0]["hash"], password):
            return apology("Invalid old password", 400)

        # Check new passwords
        elif request.form.get("new_pass_1") != request.form.get("new_pass_2"):
            return apology("Invalid password confirmation", 400)

        # Check for a duplicate
        elif password == new_pass:
            return apology("New password duplicates the old one", 400)

        # Update user's password
        db.execute("UPDATE users SET hash = :hash WHERE id = :id",
                   hash=generate_password_hash(new_pass), id=user_id)

        flash("Password successfully updated.")
        return redirect("/")

    else:
        return render_template("changepass.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
