from flask import Flask, render_template, request

app = Flask(__name__)


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
