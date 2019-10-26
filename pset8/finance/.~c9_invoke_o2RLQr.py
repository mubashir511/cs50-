import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
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
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("symbol"):
            return apology("missing symbol", 403)

        # Ensure share quantity was submitted
        if not request.form.get("shares"):
            return apology("missing shares", 403)

        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("INVALID SYMBOL")

        # Can the user afford the stock
        # Find the cash in hand
        cash = db.execute("SELECT cash FROM users WHERE id=:id", id = session["user_id"])
        userName = db.execute("SELECT username FROM users WHERE id=:id", id = session["user_id"])

        if (quote['price']*(float(request.form.get("shares")))) >= (cash[0]["cash"]):
            return("can't afford",403)

        # check is table is empty
        chk_empty = db.execute("SELECT 1 FROM buy")
        if not chk_empty:
            db.execute("INSERT INTO buy (id, username, companyName, symbol, shares, price, total) VALUES(:id, :username, :companyName, :symbol, :shares, :price, :total)",
                    username = userName[0]["username"], companyName = quote['name'], symbol = quote['symbol'], shares = request.form.get("shares"),
                    price = quote['price'], total = quote['price']*float(request.form.get("shares")), id = session["user_id"])
        else:
            # Search if the company share user is asking is already present(in hand)
            search = db.execute("SELECT * FROM buy WHERE id = :id AND symbol = :symbol", id=session["user_id"], symbol=request.form.get("symbol"))
            #print(f"search: {search}")
            #print(request.form.get("shares"))
            #print(search[0]["shares"])

            if not search:
                db.execute("INSERT INTO buy (id, username, companyName, symbol, shares, price, total) VALUES(:id, :username, :companyName, :symbol, :shares, :price, :total)",
                            username = userName[0]["username"], companyName = quote['name'], symbol = quote['symbol'], shares = request.form.get("shares"),
                            price = quote['price'], total = quote['price']*float(request.form.get("shares")), id = session["user_id"])
            else:
                # update buying data into buy table
                db.execute("UPDATE buy SET shares=:shares, price=:price, total=:total WHERE id=:id", shares = (request.form.get("shares") + search[0]["shares"]),
                            price = quote['price'], total = quote['price']*float(request.form.get("shares")), id = session["user_id"])

        # update the cash in hand
        db.execute("UPDATE users SET cash=:Cash where id=:id", Cash=((cash[0]["cash"]) - (quote['price']*float(request.form.get("shares")))), id = session["user_id"])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


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
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

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
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("symbol"):
            return apology("Missing Symbol")

        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("INVALID SYMBOL")

        return render_template("quoted.html", name=quote['name'], symbol=quote['symbol'], price=quote['price'])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure Confirm password is submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("must write same passward in both fields", 403)
        else:
            hashPass = generate_password_hash((request.form.get("password")), method ='pbkdf2:sha256', salt_length = 8)

        # check is table is empty
        chk_empty = db.execute("SELECT 1 FROM users")

        # If empty table
        if not chk_empty:
            db.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='users'")

        result = db.execute("INSERT INTO users (username,hash) VALUES(:username,:hash)",username = request.form.get("username"), hash = hashPass)

        if not result:
            return apology("user name is already in use", 403)

        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
