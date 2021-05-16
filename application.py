import os

# import sqlite3 # https://www.tutorialspoint.com/sqlite/sqlite_python.htm
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import time
import datetime
import moment
import pandas as pd

from helpers import login_required, apology, innumber #, lookup, usd 

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

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")
# db = conn.cursor()

#---------------------------------------------------

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        rows = db.execute("SELECT firstname FROM users WHERE id = ?", session["user_id"])
        firstname = rows[0]["firstname"]

        history = db.execute("SELECT *, bookings.id AS booking_id, ((bookings.end_date_int - bookings.start_date_int)/24/60/60+1) AS numberofdays FROM bookings INNER JOIN seats ON bookings.seat_id = seats.id WHERE user_id = ?", session["user_id"])

        # Number of days
        # for histor in history:
           #  numberofdays = histor["end_date_int"] - histor["start_date_int"]



        # for histor in history:
           #  numberofdays = len(pd.date_range(histor["start_date_int"],histor["end_date_int"]-datetime.timedelta(days=1), freq='d'))

           # OR

           # from datetime import date
            # >>> d1 = date(2017,3,16)
            # >>> d2 = date(2017,5,29)
            # >>> abs(d1 - d2).days
            # 74
 
        return render_template("index.html", firstname = firstname, history = history)

    # Now POST method)
    bookings = db.execute("SELECT id FROM bookings WHERE id = ?", request.form.get("bookId"))
    bookId = request.form.get("bookId")
    
    # Exceptions
    if len(bookings) != 1: 
        return apology("Such booking does not exist...weird")

    # Delete the booking
    db.execute("DELETE FROM bookings WHERE id = ?", bookId)

    # and don't forget to display all the previous exercise
    return redirect("/")
       

    #get flashed message - details are already in layouts.html
    flash("Your booking has been cancelled.")
    return render_template("index.html", firstname = firstname, history = history)
    

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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure passwords are the same
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords must be the same.")

        # Query database for username
        rows = db.execute("SELECT COUNT(*) as cnt FROM users WHERE username = ?", request.form.get("username"))

        # Ensure the username is unique
        if rows[0]["cnt"] != 0:
            return apology("username is already taken.")

        # Generate password hash
        hash = generate_password_hash(request.form.get("password"))

        # Add new registrant to database
        db.execute("INSERT INTO users (username, hash, firstname) VALUES(?, ?, ?)", request.form.get("username"), hash, request.form.get("firstname"))

        rows = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))

        session["user_id"] = rows[0]["id"]

        return redirect("/")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/book", methods=["GET", "POST"])
@login_required
def book():
    if request.method == "GET":
        seats = db.execute("SELECT id, seat_name FROM seats")
        return render_template("book.html", seats = seats, start_date = request.args.get('start_date'), end_date = request.args.get('end_date'), seat_name = request.args.get('seat_name'), seat_id = request.args.get('seat_id'))
    
    # Ensure startdate  was submitted
    if not request.form.get("istartdate"):
        return apology("must provide startdate", 400)

    # Ensure enddate was submitted
    if not request.form.get("ienddate"):
        return apology("must provide end date", 400)

    # Ensure seat is chosen
    if not request.form.get("iseat"):
        return apology("must provide seat", 400)
    
    # ensure seat exists
    rows = db.execute("SELECT * FROM seats WHERE id = ?", request.form.get("iseat"))
    if len(rows) != 1:
        return apology("seat does not exist")

    """
    istartdate = int(time.mktime(datetime.datetime.strptime(request.form.get("istartdate"), "%Y-%m-%d").timetuple()))
    print(request.form.get("istartdate"))
    print(istartdate)

    ienddate = int(time.mktime(datetime.datetime.strptime(request.form.get("ienddate"), "%Y-%m-%d").timetuple()))
    print(request.form.get("ienddate"))
    print(ienddate)
    """
    istartdate = request.form.get("istartdate")
    ienddate = request.form.get("ienddate")

    
    # check if end date is greater than startdate
    if innumber(istartdate) > innumber(ienddate):
        return apology("end date must be greater than start date")


    # compare intervals with existing bookings
    rows = db.execute("SELECT count(*) as cnt FROM bookings WHERE start_date_int <= ? AND end_date_int >= ? AND seat_id = ?", innumber(ienddate), innumber(istartdate), request.form.get("iseat"))
    if rows[0]["cnt"] > 0:
        return apology("Sorry, the seat is taken", 400)

    # insert into bookings
    bookings = db.execute("INSERT INTO bookings(seat_id, start_date, start_date_int, end_date, end_date_int, user_id) VALUES (?,?,?,?,?,?)", request.form.get("iseat"), istartdate, innumber(istartdate), ienddate, innumber(ienddate), session["user_id"])
    
    return redirect("/")

@app.route("/calendar", methods=["GET", "POST"])
@login_required
def calendar():
    if request.method == "GET":
        return render_template("calendar.html")



@app.route("/seating", methods=["GET", "POST"])
@login_required
def seating():
    if request.method == "GET":
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        today_int = innumber(today)
        ids = db.execute("SELECT user_id, seat_id FROM bookings INNER JOIN seats ON bookings.seat_id = seats.id WHERE start_date_int <= ? AND end_date_int >= ?", today_int, today_int)
        current_user = session['user_id']
        print(ids)
        return render_template("seating.html", today = today, ids = ids, current_user = current_user)
    else:
        today = request.form.get("today")
        today_int = innumber(today)
        ids = db.execute("SELECT user_id, seat_id FROM bookings INNER JOIN seats ON bookings.seat_id = seats.id WHERE start_date_int <= ? AND end_date_int >= ?", today_int, today_int)
        current_user = session['user_id']
        print(ids)
        return render_template("seating.html", today = today, ids = ids, current_user = current_user)
        
        

        

