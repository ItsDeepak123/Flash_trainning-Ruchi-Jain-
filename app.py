from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def Home():
    return "This is First Page"


@app.route("/welcome")
def welcome():
    return "This is second page"


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/success/<float:a>")
def success(a):
    return "The person is pass and the score is " + str(a)


@app.route("/fail/<float:a>")
def fail(a):
    return "You are fail and the score is " + str(a)


@app.route("/calculate", methods=["POST", "GET"])
def calculate():

    if request.method == "GET":
        return render_template("calculate.html")

    else:
        maths = float(request.form["maths"])
        science = float(request.form["science"])
        history = float(request.form["history"])

        avg = (maths + science + history) / 3

        if avg > 80:
            return redirect(url_for("success", a=avg))
        else:
            return redirect(url_for("fail", a=avg))


if __name__ == "__main__":
    app.run(debug=True)