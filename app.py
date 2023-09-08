from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)

# Initialize session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize database with cs50 library
db = SQL("sqlite:///todotitan.db")

# SQL table structure
# CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username UNIQUE TEXT NOT NULL, hash TEXT NOT NULL);
# CREATE TABLE tasks (task_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, task_text TEXT NOT NULL, user_id INTEGER NOT NULL);
def login_required(f):
    '''Code from CS50 finance'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def error(message):
    return render_template("error.html", message=message)

@app.route("/", methods=["GET", "POST"])
def homepage():
    tasks = []
    if request.method == "GET":
        return render_template("index.html")
    else:
        tasks.append(request.form.get("task"))
        return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    # TODO remove task from database
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Reset session
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check username and password are submitted
        if not request.form.get("username") or not request.form.get("password"):
            return error("Submitted fields cannot be blank")
        
        user = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0]["hash"], request.form.get("password")):
            return error("Invalid login information")

        # store account login status until session is cleared
        session["account_id"] = user[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # if form was submitted via post, get form info and check validity
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # check username valididty
        if not username:
            return error("Username field cannot be empty")

        for entry in db.execute("SELECT username FROM users;"):
            if username == entry["username"]:
                return error("Username is already taken")

        # check password valididty
        if password != confirmation or (not password) or (not confirmation):
            return error("Invalid Password")
        elif len(password) < 8:
            return error("Password Must be at Least 8 Characters Long")

        db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?);",
            username,
            generate_password_hash(password),
        )
        return redirect("/")
    else:
        return render_template("register.html")


