# to get environment variables
# and to generate random hash
import os

# for token storage
import binascii

# for parametarization
from cs50 import SQL
#flask functionality
from flask import Flask, jsonify, redirect, render_template, request, session
#for cookies setting
from flask_session import Session
#to set cookies in a temp file not in browser
from tempfile import mkdtemp
#for exception handling
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
#for password hashing and checking
from werkzeug.security import check_password_hash, generate_password_hash

#for connecting and executing queries
import mysql.connector
#for SQL error handling
from mysql.connector import errorcode

#login_required & admin_required decorators, error page, and check_admins
from helpers1 import login_required,admin_required, apology, check_admins, check_admin_cookies

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#set db as global variable
db = ""
#Load database at first request
@app.before_first_request
def before_first_request_func():
    
    # Make sure admins are set
    check_admins()
    
    DB_NAME= "Labs"
    
    try:
        cnx = mysql.connector.connect(user='root',password=os.environ.get("sqlpass"),host='127.0.0.1',charset='utf8mb4')
        db = cnx.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        else:
            print(err)
	
    try:
        db.execute("USE {}".format(DB_NAME))
        print("Database already exists and in use")
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        print(err)


#check for cookies
def check_cookies():
    db.execute("SELECT * FROM users WHERE username = :username AND token = :token LIMIT 1",
               username = session.get("username"),token = session.get("token"))
    cookie = db.fetchone()
    if cookie is None:
        return render_template("banned.html")
    return True


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


@app.route("/")
@login_required
def index():
    check_cookies()
    #TODO
    return apology("Not set", 400)

@app.route("/admin")
@admin_required
def admin_index():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any cookies set
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
        db.execute("SELECT * FROM users WHERE username = :username LIMIT 1",username=request.form.get("username"))
        rows = db.fetchone()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["token"] = rows[0]["token"]
        session["username"] = rows[0]["username"]

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
        
        db.execute("SELECT username FROM users WHERE username = :username LIMIT 1", username = request.form.get("username"))
        user_exist = db.fetchone()
        
        if not user_exist:
            return apology("Username already exists", 400)

        hasher = generate_password_hash(request.form.get("password"))
        
        token = binascii.hexlify(os.urandom(16))
        
        if not request.form.get("insurance") or request.form.get("insurance")== '':
            db.execute("insert into patient_essentials (name) values ('{name}');".format(name = request.form.get("name")))
            db.execute("insert into patient_extras (SSN, sex, phone, bdate, blood_type, street, district, province)"
                       "values ('{SSN}', '{sex}', '{phone}', '{bdate}', '{blood_type}', '{street}', '{district}', '{province}')".format(SSN = request.form.get("SSN"), sex = request.form.get("sex"),
                       phone = request.form.get("phone"), bdate = request.form.get("bdate"), blood_type = request.form.get("blood_type"),
                       street = request.form.get("street"), district = "TODO", province = request.form.get("province")))
        else:
            db.execute("insert into patient_essentials (name, insurance) values ('{name}', '{insurance}');".format(name = request.form.get("name"), insurance = request.form.get("insurance")))
            db.execute("insert into patient_extras (SSN, sex, phone, bdate, blood_type, street, district, province)"
                       "values ('{SSN}', '{sex}', '{phone}', '{bdate}', '{blood_type}', '{street}', '{district}', '{province}')".format(SSN = request.form.get("SSN"),
                       sex = request.form.get("sex"), phone = request.form.get("phone"), bdate = request.form.get("bdate"), blood_type = request.form.get("blood_type"),
                       street = request.form.get("street"), district = "TODO", province = request.form.get("province")))

        db.execute("insert into users (username, hash, token, email) values ('{username}', '{hashed}', '{token}', '{email}')".format(username = request.form.get("username"), hashed=hasher, token = token, email = request.form.get("email")))
        
        # automatically login
        session["token"] = token
        session["username"] = request.form.get("username")
        return redirect("/")


@app.route("/patient_access", methods=["GET", "POST"])
@admin_required
def pat_acc():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
	
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)


@app.route("/devices")
@admin_required
def device():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)


@app.route("/view_devices")
@admin_required
def view_device():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)


@app.route("/modify_device", methods=["GET", "POST"])
@admin_required
def mod_device():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)



@app.route("/add_device", methods=["GET", "POST"])
@admin_required
def add_device():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)



@app.route("/delete_devices", methods=["GET", "POST"])
@admin_required
def del_device():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)



@app.route("/analytics")
@admin_required
def analytic():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)


@app.route("/view_analytics")
@admin_required
def view_analytic():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)


@app.route("/modify_analytic", methods=["GET", "POST"])
@admin_required
def mod_analytic():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)



@app.route("/add_analytic", methods=["GET", "POST"])
@admin_required
def add_analytic():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)



@app.route("/delete_analytics", methods=["GET", "POST"])
@admin_required
def del_analytic():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)



@app.route("/staff")
@admin_required
def staff():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)


@app.route("/view_staff")
@admin_required
def view_staff():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)


@app.route("/modify_staff", methods=["GET", "POST"])
@admin_required
def mod_staff():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)



@app.route("/add_staff", methods=["GET", "POST"])
@admin_required
def add_staff():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)



@app.route("/delete_staff", methods=["GET", "POST"])
@admin_required
def del_staff():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)



@app.route("/depend")
@admin_required
def depend():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)


@app.route("/view_depend")
@admin_required
def view_depend():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)

@app.route("/add_depend", methods=["GET", "POST"])
@admin_required
def add_depend():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)



@app.route("/delete_depend", methods=["GET", "POST"])
@admin_required
def del_depend():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)


@app.route("/schedule", methods=["GET", "POST"])
@admin_required
def schedule():
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)
    

@app.route("/tests")
@admin_required
def tests():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)


@app.route("/view_tests")
@admin_required
def view_tests():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)


@app.route("/add_result", methods=["GET", "POST"])
@admin_required
def add_result():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)


@app.route("/add_medcon", methods=["GET", "POST"])
@admin_required
def add_medcon():
    check_admin_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)


@app.route("/log")
@admin_required
def log():
    check_admin_cookies()
    #TODO
    return apology("Not set", 400)

@app.route("/book_test")
@login_required
def book_test():
    check_cookies()
    #TODO
    return apology("Not set", 400)


@app.route("/booking", methods=["GET", "POST"])
@admin_required
def booking():
    check_cookies()
    if request.method == "GET":
        #TODO
        return apology("Not set", 400)
    
    if request.method == "POST":
        #TODO
        return apology("Not set", 400)


@app.route("/results")
@login_required
def results():
    check_cookies()
    #TODO
    return apology("Not set", 400)
    


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("error.html",e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
