# Create a virtual environment
# https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/

# Import the Python OS Module - provides functions for interacting with the operating system
import os

# CS50 library includes functionality to interact with SQL databases with ease
# https://cs50.readthedocs.io/libraries/cs50/python/
# CS50 includes wheel, typing-extensions, termcolor, sqlparse, packaging, greenlet, SQLAlchemy, cs50
# CS50 installed termcolor, packaging, MarkupSafe, itsdangerous, greenlet, colorama, blinker, Werkzeug, SQLAlchemy, Jinja2, click, Flask, cs50
from cs50 import SQL

# Install flask within the activated .venv environment.
# https://flask.palletsprojects.com/en/3.0.x/installation/
from flask import Flask, render_template, redirect, request, session
# Install flask_session.
# https://flask-session.readthedocs.io/en/latest/installation.html
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import get_parks, find_borough, borough_name

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies) - CS50 Design
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

"""
CS50 Finance Notes - https://cs50.harvard.edu/x/2023/psets/9/finance/
Within finance/, run sqlite3 finance.db to open finance.db with sqlite3. If you run .schema in the SQLite prompt, notice how finance.db comes with a table called users. 
Take a look at its structure (i.e., schema). Notice how, by default, new users will receive $10,000 in cash. But if you run SELECT * FROM users;, there aren’t (yet!) any users (i.e., rows) therein to browse.

Another way to view finance.db is with a program called phpLiteAdmin. Click on finance.db in your codespace’s file browser, then click the link shown underneath the text “Please visit the following link to authorize GitHub Preview”. 
You should see information about the database itself, as well as a table, users, just like you saw in the sqlite3 prompt with .schema.
"""

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///parks.db")

# CS50 Design
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# https://stackoverflow.com/questions/32019733/getting-value-from-select-tag-using-flask
@app.route("/")
def index():
    """Show all Parks"""

    # Ensure user is logged in
    if session.get("user_id") is None:
        return render_template("start.html")
    else:
        parks = get_parks()

        name = request.form.get('name')

        borough_name(name)

        return render_template("index.html", parks=parks, borough_name=borough_name)


@app.route("/borough", methods=["GET", "POST"])
def borough():
    """Show parks in the borough selected by the user"""

    if session.get("user_id") is None:
        return render_template("start.html")
    else:
        name = request.form.get('name')

        borough = find_borough(name)

        borough_name(name)

        return render_template("borough.html", borough=borough, borough_name=borough_name)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            message = "Please provide username"
            return render_template("login.html", message=message)

        # Ensure password was submitted
        elif not request.form.get("password"):
            message = "Please provide password"
            return render_template("login.html", message=message)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            message = "Invalid username and/or password"
            return render_template("login.html", message=message)

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
            message = "Please provide username"
            return render_template("register.html", message=message)

        # Ensure password was submitted
        elif not request.form.get("password"):
            message = "Please provide password"
            return render_template("register.html", message=message)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            message = "Please provide password confirmation"
            return render_template("register.html", message=message)

        # Ensure password and password confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            message = "Passwords must match"
            return render_template("register.html", message=message)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username does not exist
        if len(rows) != 0:
            message = "Username already taken"
            return render_template("register.html", message=message)

        # Generate password hash
        password = request.form.get("password")
        hash = generate_password_hash(password)

        # Store username
        username = request.form.get("username")

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Get user id from users table
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = user_id[0]["id"]

        # Redirect user to home page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:        
        return render_template("register.html")


# Instructions to run the program via the command python app.py
if __name__ == '__main__':
    app.run()
    # app.run(debug=True)