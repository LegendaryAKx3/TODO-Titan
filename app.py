from functools import wraps

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from flask_session import Session

app = Flask(__name__)

# Initialize session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize database with cs50 library
db = SQL("sqlite:///todotitan.db")


# SQL table structure
def login_required(f):
    """Code from CS50 finance"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("uuid") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def error(message):
    return render_template(
        "index.html",
        error=message,
        tasks=db.execute(
            "SELECT * FROM tasks WHERE uuid = ? ORDER BY timestamp ASC", session["uuid"]
        ),
        sections=db.execute("SELECT * FROM sections WHERE uuid = ?", session["uuid"]),
    )


@app.route("/", methods=["GET", "POST"])
@login_required
def homepage():
    if request.method == "GET":
        return render_template(
            "index.html",
            tasks=db.execute(
                "SELECT * FROM tasks WHERE uuid = ? ORDER BY timestamp ASC",
                session["uuid"],
            ),
            sections=db.execute(
                "SELECT * FROM sections WHERE uuid = ?", session["uuid"]
            ),
        )
    else:
        # Only add section id to db if section is specified
        if request.form.get("section") != "":
            db.execute(
                "INSERT INTO tasks (task_text, uuid, section_id) VALUES(?, ?, ?);",
                request.form.get("task"),
                session["uuid"],
                request.form.get("section"),
            )
        else:
            db.execute(
                "INSERT INTO tasks (task_text, uuid) VALUES(?, ?);",
                request.form.get("task"),
                session["uuid"],
            )
        return redirect("/")


@app.route("/section-create", methods=["POST"])
@login_required
def create_section():
    name = request.form.get("section")
    # Prevent duplicate sections
    user_sections = db.execute("SELECT * FROM sections WHERE uuid = ?", session["uuid"])
    for section in user_sections:
        if section["section_name"].lower() == name.lower():
            return error("Duplicate section name")
    # Prevent empty section names

    if name.strip() == "":
        return error("Section name cannot be empty")

    db.execute(
        "INSERT INTO sections (section_name, uuid) VALUES(?, ?);",
        name.title(),
        session["uuid"],
    )
    return redirect("/")


@app.route("/section-delete-all", methods=["POST"])
@login_required
def delete_section_all():
    """Delete section and tasks within it"""
    # Delete section from section table where section and user id match up
    # won't go through if user not logged in to the account corresponding to the section
    db.execute(
        "DELETE FROM sections WHERE (section_id = ? AND uuid = ?);",
        request.form.get("section-id"),
        session["uuid"],
    )

    # delete tasks within deleted section
    db.execute(
        "DELETE FROM tasks WHERE (section_id = ? AND uuid = ?);",
        request.form.get("section-id"),
        session["uuid"],
    )
    return redirect("/")


@app.route("/move-between-section", methods=["POST"])
@login_required
def move_between_section():
    """Move task between sections"""
    section_to = request.form.get("to-section")
    task_id = request.form.get("task-id")
    if (
        db.execute("SELECT * FROM tasks WHERE(task_id = ?);", task_id)[0]["uuid"]
        != session["uuid"]
    ):
        error("Invalid request")

    if section_to != "":
        db.execute(
            "UPDATE tasks SET section_id = ? WHERE (task_id = ? AND uuid = ?);",
            section_to,
            task_id,
            session["uuid"],
        )
    else:
        db.execute(
            "UPDATE tasks SET section_id = NULL WHERE (task_id = ? AND uuid = ?);",
            task_id,
            session["uuid"],
        )
    return redirect("/")


@app.route("/section-delete", methods=["POST"])
@login_required
def delete_section():
    """Delete section and send all contained tasks to main section"""
    # Delete section where section and user id match up
    # won't go through if user not logged in to the account corresponding to the section
    db.execute(
        "DELETE FROM sections WHERE (section_id = ? AND uuid = ?);",
        request.form.get("section-id"),
        session["uuid"],
    )

    # Send all contained tasks to main section
    db.execute(
        "UPDATE tasks SET section_id = NULL WHERE (section_id = ? AND uuid = ?);",
        request.form.get("section-id"),
        session["uuid"],
    )
    return redirect("/")


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    # Delete task where task and user id match up
    # won't go through if user is not logged in to the account corresponding to the task
    db.execute(
        "DELETE FROM tasks WHERE (uuid = ? AND task_id = ?);",
        session["uuid"],
        request.form.get("id"),
    )
    return redirect("/")

@app.route("/edit_note", methods=["POST"])
@login_required
def edit_note():
    # Edit/Add note to user's task
    db.execute("UPDATE tasks SET task_note = ? WHERE uuid = ? AND task_id = ?",
                request.form.get("note"), 
                session["uuid"], 
                request.form.get("task-id"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Code based on login from CS50 finance"""
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check both username and password are submitted
        if (not request.form.get("username")) or (not request.form.get("password")):
            return render_template(
                "login.html", error="Please enter both username and password"
            )

        user = db.execute(
            "SELECT * FROM accounts WHERE username = ?", request.form.get("username")
        )
        # Ensure username exists and password is correct

        # HACK: len(user) != 1?
        if len(user) != 1 or not check_password_hash(
            user[0]["hash"], request.form.get("password")
        ):
            return render_template("login.html", error="Invalid login information")

        # store account login status until session is cleared
        session["uuid"] = user[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Code based on logout from CS50 finance"""
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user (Personal code from CS50 Finance)"""
    if request.method == "POST":
        # get form info and check validity

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return render_template(
                "register.html", error="Username field cannot be empty"
            )

        for entry in db.execute("SELECT username FROM accounts;"):
            if username == entry["username"]:
                return render_template(
                    "register.html", error="Username is Already Taken"
                )

        # check password valididty
        if password != confirmation or (not password) or (not confirmation):
            return render_template(
                "register.html", error="Invalid password or confirmation"
            )

        elif (len(password) < 8) or (password.lower() == password):
            return render_template(
                "register.html",
                error="Password Must be at Least 8 Characters Long and Contain a Capital Letter",
            )

        db.execute(
            "INSERT INTO accounts (username, hash) VALUES(?, ?);",
            username,
            generate_password_hash(password),
        )
        return redirect("/")
    return render_template("register.html")

