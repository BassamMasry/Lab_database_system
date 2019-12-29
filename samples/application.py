from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers1 import login_required

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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Make sure admins are set
check_admins()

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    shares = db.execute("SELECT share,number FROM shares WHERE user_id = :id", id=session['user_id'])
    casher = db.execute("SELECT cash from users WHERE id = :id", id=session['user_id'])
    cash = float('%.2f' % (casher[0]['cash']))
    price = []
    total = []
    rows = []
    sumer = 0
    for index, row in enumerate(shares):
        looker = lookup(row['share'])
        price.append(looker['price'])
        total.append(float('%.2f' % (price[index] * row['number'])))
        rows.append((row['share'], row['number'], price[index], total[index]))
        sumer += total[index]

    return render_template("index.html", rows=rows, cash=cash, total=cash + sumer)

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
        rows = db.execute("SELECT * FROM users WHERE username = :username",username=request.form.get("username"))

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

    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation do not match", 400)

        hasher = generate_password_hash(request.form.get("password"))

        result = db.execute("insert into users (username, hash) values (:username, :hashed)",
                    username = request.form.get("username"), hashed=hasher)
        if not result:
            return apology("Username already exists", 400)

        # automatically login
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":
        count = request.form.get("shares")
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        elif not count:
            return apology("must provide count", 400)

        elif not count.isnumeric():
            return apology("Must enter a positive number", 400)

        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session['user_id'])
        quoter = lookup(request.form.get("symbol"))
        if not quoter:
            return apology("Enter a valid symbol", 400)
        price = quoter["price"]
        counter = int(count)
        if cash[0]["cash"] > (counter * price):
            db.execute("INSERT INTO history (user_id,share,date,num,price,buy_sell) VALUES (:id,:symbol,datetime('now'),:count,:price,'b')",
                id=session["user_id"],symbol=request.form.get("symbol"), count = counter, price=price)
            share_exist = db.execute("SELECT share,number from shares where user_id = :id and share = :share",
                     id = session["user_id"], share=request.form.get("symbol"))
            if not share_exist:
                db.execute("INSERT INTO shares (user_id,share,number) VALUES (:id,:symbol,:count)",
                     id=session["user_id"],symbol=request.form.get("symbol"), count = counter)
            else:
                db.execute("UPDATE shares set number = :num where user_id = :id and share = :share",
                        num = share_exist[0]["number"]+counter, id=session["user_id"], share=request.form.get("symbol"))
            db.execute("UPDATE users SET cash = :cash where id = :id",
                 cash = cash[0]["cash"] - (counter * price), id=session["user_id"])
            return redirect("/")
        else:
            return apology("You do not have enough money", 400)


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    users = db.execute("SELECT id from users WHERE username = :user", user=username)
    if not users:
        return jsonify(True)
    return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT share,date,num,price,Buy_Sell from history WHERE user_id = :id", id=session['user_id'])
    return render_template("history.html", rows=rows)


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":
        symbol = request.form.get("symbol")
        if symbol != None:
            if symbol == "":
                return apology("must provide symbol", 400)
            else:
                quoter = lookup(symbol)
                if not quoter:
                    return apology("Enter a valid symbol", 400)
                return render_template("quoted.html", quoter=quoter)
        if symbol == None:
            return apology("must provide symbol", 400)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        rows = db.execute("SELECT share from shares where user_id = :id", id=session["user_id"])
        options = []
        for row in rows:
            options.append(row['share'])
        return render_template("sell.html", options=options)

    if request.method == "POST":
        rows = db.execute("SELECT share,number from shares where user_id = :id", id=session["user_id"])
        symbol = request.form.get("symbol")
        count = request.form.get("shares")
        indexer = 0
        if not symbol:
            return apology("must provide symbol", 400)

        for index, row in enumerate(rows):
            if symbol != row['share']:
                continue
            else:
                indexer = index
                break
            return apology("you dont have this share", 400)

        if not count:
            return apology("must provide count", 400)

        elif int(count) > rows[index]['number']:
            return apology("you do not have enough shares", 400)

        elif not count.isnumeric():
            return apology("Enter a positive number for count", 400)

        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session['user_id'])
        counter = int(count)
        quoter = lookup(symbol)
        if not quoter:
            return apology("Enter a valid symbol", 400)
        price = quoter["price"]
        db.execute("INSERT INTO history (user_id,share,date,num,price,buy_sell) VALUES (:id,:symbol,datetime('now'),:count,:price,'s')",
                    id=session["user_id"], symbol=symbol, count=counter, price=price)

        if counter == rows[indexer]['number']:
            db.execute("DELETE FROM shares where user_id = :id and share = :share", id=session["user_id"], share=symbol)
        else:
            db.execute("UPDATE shares set number = :num where user_id = :id and share = :share",
                        num=rows[indexer]["number"]-counter, id=session["user_id"], share=rows[indexer]['share'])

        db.execute("UPDATE users SET cash = :cash where id = :id", cash=cash[0]["cash"] + (counter * price), id=session["user_id"])

        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("error.html",e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
