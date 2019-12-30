import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, Response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, pkr, price
from datetime import datetime, date

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
app.jinja_env.filters["pkr"] = pkr

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pay.db")


@app.route("/prices", methods=["GET", "POST"])
@login_required
def prices():
    """Show prices of the Products"""
    # Get prices from "price Class"

    prices = price()

    return render_template("prices.html", prices=prices)


@app.route("/")
@login_required
def index():
    """Show portfolio of buying"""
    # search buy table
    search_buy = db.execute("SELECT * FROM buy WHERE id=:id", id=session["user_id"])
    # find the max length of the search data
    search_len = len(search_buy)

    # Search cash table for remaing cash in hand
    search_users = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

    # update the grand total
    totals = db.execute("SELECT total FROM buy WHERE id=:id", id=session["user_id"])
    big_total = 0
    for i in range(search_len):
        big_total += totals[i]['total']
    
    return render_template("index.html", search_buy=search_buy, search_len=search_len, search_users=search_users,big_total=big_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy goods"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        class quantity:
            rice = request.form.get("rice_Quantity")
            flour = request.form.get("flour_Quantity")
            sugar = request.form.get("sugar_Quantity")

        buyProduct = quantity()
        productPrice = price()

        # Check is all fields are empty
        if (not buyProduct.rice and not buyProduct.sugar and not buyProduct.flour):
            return apology("Provide product quantity")
        else:

            if not (not buyProduct.rice):
                # Validate input value for rice
                if ((isinstance(buyProduct.rice, float)) and (buyProduct.rice <= 0)):
                    return apology("Provide valid input")
                else:
                    # get present cash in hand value
                    cashInHand = db.execute("SELECT cash FROM users WHERE id=:id",
                                            id=session["user_id"])
                                            
                    # Is ask price is more than cash in hand
                    if (((int(productPrice.rice) * int(buyProduct.rice))) > (cashInHand[0]["cash"])):
                        return apology("You have insufficient cash for rice")

                    # Check if rice is previously bought
                    checkRice = db.execute("SELECT * FROM buy WHERE id=:id AND product=:product",
                                           id=session["user_id"],
                                           product="rice")
                    if not checkRice:
                        # Insert bought value in the buy table
                        db.execute("INSERT INTO buy (id,product,quantity,price,total) VALUES(:id,:product,:quantity,:price,:total)",
                                   id=session["user_id"],
                                   product="rice",
                                   quantity=buyProduct.rice,
                                   price=productPrice.rice,
                                   total=(int(productPrice.rice) * int(buyProduct.rice)))
                    else:
                        db.execute("UPDATE buy SET quantity=:quantity, price=:price, total=:total WHERE id=:id AND product=:product",
                                   quantity=int(checkRice[0]["quantity"]) + int(buyProduct.rice),
                                   price=productPrice.rice,
                                   total=int(checkRice[0]["total"]) + (int(productPrice.rice) * int(buyProduct.rice)),
                                   id=session["user_id"],
                                   product="rice")

                    # getting current time
                    now = datetime.now()
                    # hr:min:sec
                    current_time = now.strftime("%H:%M:%S")

                    # Getting current date
                    today = date.today()
                    # Textual month, day and year
                    current_date = today.strftime("%B %d, %Y")

                    # Insert bought value in history table
                    db.execute("INSERT INTO history (id,product,quantity,price,time,date) VALUES(:id,:product,:quantity,:price,:time,:date)",
                               id=session["user_id"],
                               product="rice",
                               quantity=buyProduct.rice,
                               price=productPrice.rice,
                               time=current_time,
                               date=current_date)

                    # update cash value in users table
                    db.execute("UPDATE users SET cash=:cash WHERE id=:id",
                               cash=(cashInHand[0]["cash"] - (int(productPrice.rice) * int(buyProduct.rice))),
                               id=session["user_id"])

            if not (not buyProduct.sugar):
                # Validate input value for sugar
                if ((isinstance(buyProduct.sugar, float)) and (buyProduct.sugar <= 0)):
                    return apology("Provide valid input")
                else:
                    # get present cash in hand value
                    cashInHand = db.execute("SELECT cash FROM users WHERE id=:id",
                                            id=session["user_id"])

                    # Is ask price is more than cash in hand
                    if (((int(productPrice.sugar) * int(buyProduct.sugar))) > (cashInHand[0]["cash"])):
                        return apology("You have insufficient cash for sugar")

                    # Check if sugar is previously bought
                    checkSugar = db.execute("SELECT * FROM buy WHERE id=:id AND product=:product",
                                           id=session["user_id"],
                                           product="sugar")
                    if not checkSugar:
                        # Insert bought value in the buy table
                        db.execute("INSERT INTO buy (id,product,quantity,price,total) VALUES(:id,:product,:quantity,:price,:total)",
                                   id=session["user_id"],
                                   product="sugar",
                                   quantity=buyProduct.sugar,
                                   price=productPrice.sugar,
                                   total=(int(productPrice.sugar) * int(buyProduct.sugar)))
                    else:
                        db.execute("UPDATE buy SET quantity=:quantity, price=:price, total=:total WHERE id=:id AND product=:product",
                                   quantity=int(checkSugar[0]["quantity"]) + int(buyProduct.sugar),
                                   price=productPrice.sugar,
                                   total=int(checkSugar[0]["total"]) + (int(productPrice.sugar) * int(buyProduct.sugar)),
                                   id=session["user_id"],
                                   product="sugar")

                    # getting current time
                    now = datetime.now()
                    # hr:min:sec
                    current_time = now.strftime("%H:%M:%S")

                    # Getting current date
                    today = date.today()
                    # Textual month, day and year
                    current_date = today.strftime("%B %d, %Y")

                    # Insert bought value in history table
                    db.execute("INSERT INTO history (id,product,quantity,price,time,date) VALUES(:id,:product,:quantity,:price,:time,:date)",
                               id=session["user_id"],
                               product="sugar",
                               quantity=buyProduct.sugar,
                               price=productPrice.sugar,
                               time=current_time,
                               date=current_date)

                    # update cash value in users table
                    db.execute("UPDATE users SET cash=:cash WHERE id=:id",
                               cash=(cashInHand[0]["cash"] - (int(productPrice.sugar) * int(buyProduct.sugar))),
                               id=session["user_id"])

            if not (not buyProduct.flour):
                # Validate input value for flour
                if ((isinstance(buyProduct.flour, float)) and (buyProduct.flour <= 0)):
                    return apology("Provide valid input")
                else:
                    # get present cash in hand value
                    cashInHand = db.execute("SELECT cash FROM users WHERE id=:id",
                                            id=session["user_id"])

                    # Is ask price is more than cash in hand
                    if (((int(productPrice.flour) * int(buyProduct.flour))) > (cashInHand[0]["cash"])):
                        return apology("You have insufficient cash for flour")

                    # Check if sugar is previously bought
                    checkFlour = db.execute("SELECT * FROM buy WHERE id=:id AND product=:product",
                                           id=session["user_id"],
                                           product="flour")
                    if not checkFlour:
                        # Insert bought value in the buy table
                        db.execute("INSERT INTO buy (id,product,quantity,price,total) VALUES(:id,:product,:quantity,:price,:total)",
                               id=session["user_id"],
                               product="flour",
                               quantity=buyProduct.flour,
                               price=productPrice.flour,
                               total=(int(productPrice.flour) * int(buyProduct.flour)))
                    else:
                        db.execute("UPDATE buy SET quantity=:quantity, price=:price, total=:total WHERE id=:id AND product=:product",
                                   quantity=int(checkFlour[0]["quantity"]) + int(buyProduct.flour),
                                   price=productPrice.flour,
                                   total=int(checkFlour[0]["total"]) + (int(productPrice.flour) * int(buyProduct.flour)),
                                   id=session["user_id"],
                                   product="flour")

                    # getting current time
                    now = datetime.now()
                    # hr:min:sec
                    current_time = now.strftime("%H:%M:%S")

                    # Getting current date
                    today = date.today()
                    # Textual month, day and year
                    current_date = today.strftime("%B %d, %Y")

                    # Insert brought value in history table
                    db.execute("INSERT INTO history (id,product,quantity,price,time,date) VALUES(:id,:product,:quantity,:price,:time,:date)",
                               id=session["user_id"],
                               product="flour",
                               quantity=buyProduct.flour,
                               price=productPrice.flour,
                               time=current_time,
                               date=current_date)

                    # update cash value in users table
                    db.execute("UPDATE users SET cash=:cash WHERE id=:id",
                               cash=(cashInHand[0]["cash"] - (int(productPrice.flour) * int(buyProduct.flour))),
                               id=session["user_id"])

        flash("Brought!")
        return redirect("/buy")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Get user name from html form
    get_username = request.args.get("username")

    # validate the username from database
    if not len(get_username) < 1:
        username = db.execute(
            "SELECT * FROM users WHERE username=:username", username=get_username)

        if username:
            return jsonify(False)
        else:
            return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # search 'History' table
    search_history = db.execute(
        "SELECT * FROM history WHERE id=:id", id=session["user_id"])
    # find the max length of the search data
    search_len = len(search_history)

    return render_template("history.html", search_history=search_history, search_len=search_len)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure Confirm password is submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # print(((request.form.get("username")).isalnum()) or ((request.form.get("username")).isalpha()))

        # Ensure username is alphanumeric string
        if (((request.form.get("username")).isalnum()) or ((request.form.get("username")).isalpha())) == False:
            return apology("must provide aplhanumeric username", 403)

        # If passwords donot match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("must write same passward in both fields", 400)
        else:
            hashPass = generate_password_hash(
                (request.form.get("password")), method='pbkdf2:sha256', salt_length=8)

        # check is table is empty
        chk_empty = db.execute("SELECT 1 FROM users")

        # If empty table
        if not chk_empty:
            db.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='users'")

        # Set id sequence
        max_id = db.execute("SELECT MAX(id) FROM buy")
        db.execute("UPDATE SQLITE_SEQUENCE SET SEQ=:id WHERE NAME='users'",
                   id=max_id[0]['MAX(id)'])

        result = db.execute("INSERT INTO users (username,hash) VALUES(:username,:hash)",
                            username=request.form.get("username"),
                            hash=hashPass)

        if not result:
            return apology("username already taken", 400)

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change Password of user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # user ask to change username
        if request.form.get("select") == "username":
            return redirect("/changeUsername")

        # user ask to change password
        elif request.form.get("select") == "password":
            return redirect("/changePassword")

        # no input
        else:
            return apology("choose any option", 403)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change.html")


@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure old password was submitted
        if not request.form.get("old_password"):
            return apology("must provide present password", 400)

        # Ensure new password was submitted
        if not request.form.get("new_password"):
            return apology("must provide new password", 400)

        # Ensure Confirm password is submitted
        if not request.form.get("confirm_password"):
            return apology("must fill confirm password", 400)

        # Ensure Confirmation (both passwords are same)
        if (request.form.get("new_password")) != (request.form.get("confirm_password")):
            return apology("must confirm password", 400)

        # acquire hash value of present user
        present_password_hash = db.execute("SELECT hash FROM users WHERE id=:id",
                                           id=session["user_id"])

        # Ensure old password is correct
        if check_password_hash(present_password_hash[0]['hash'], request.form.get("old_password")):

            # Generate hash for new password
            new_password_hash = generate_password_hash(
                (request.form.get("new_password")), method='pbkdf2:sha256', salt_length=8)

            # Update present hash value
            db.execute("UPDATE users SET hash=:hash WHERE id=:id",
                       id=session["user_id"],
                       hash=new_password_hash)
        else:
            return apology("Provide correct password", 400)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changePassword.html")


@app.route("/changeUsername", methods=["GET", "POST"])
@login_required
def changeUsername():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("new_username"):
            return apology("must provide new username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure username is alphanumeric string
        if (((request.form.get("new_username")).isalnum()) or ((request.form.get("new_username")).isalpha())) == False:
            return apology("must provide aplhanumeric username", 403)

        # acquire hash value of present user
        password_hash = db.execute("SELECT hash FROM users WHERE id=:id",
                                   id=session["user_id"])

        # Ensure old password is correct
        if check_password_hash(password_hash[0]['hash'], request.form.get("password")):

            # Update present username from table
            db.execute("UPDATE users SET username=:username WHERE id=:id",
                       id=session["user_id"],
                       username=request.form.get("new_username"))
        else:
            return apology("Provide correct password", 400)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changeUsername.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port="5000")
