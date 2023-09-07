from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/create", methods=["POST"])
def create():
    task = request.form.get("task")
    return render_template("task_success.html", task=task)
