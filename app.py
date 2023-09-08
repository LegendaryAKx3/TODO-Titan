from flask import Flask, render_template, request, redirect
from cs50 import SQL

app = Flask(__name__)


# Initialize database with cs50 library
db = SQL("sqlite:///todotitan.db")

# SQL table structure
# CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username UNIQUE TEXT NOT NULL, hash TEXT NOT NULL);
# CREATE TABLE tasks (task_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, task_text TEXT NOT NULL, user_id INTEGER NOT NULL);

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



