from flask import Flask, render_template, request

app = Flask(__name__)

# SQL table structure
# CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username UNIQUE TEXT NOT NULL, hash TEXT NOT NULL);
# CREATE TABLE tasks (task_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, task_text TEXT NOT NULL);

@app.route("/", methods=["GET", "POST"])
def homepage():
    tasks = []
    if request.method == "GET":
        return render_template("index.html")
    else:
        tasks.append(request.form.get("task"))
        return render_template("index.html", tasks=tasks)


@app.route("/create", methods=["POST"])
def create():
    return render_template("task_success.html", name=request.args.get("name", "world"))
