from flask import Flask, render_template, request, redirect, url_for

app=Flask(__name__)


@app.route("/sum/<int:a>")
def sum(a):
    return "Total of Two values is"+str(a)

@app.route("/sub/<int:a>")
def sub(a):
    return "subtract of Two values is"+str(a)

@app.route("/mul/<int:a>")
def mul(a):
    return "multiplication of Two values is"+str(a)

@app.route("/div/<int:a>")
def div(a):
    return "division of Two values is"+str(a)



@app.route("/calculate", methods=["GET", "POST"])
def calculate1():

    result = None

    if request.method == "POST":

        var1 = float(request.form["A"])
        var2 = float(request.form["B"])

        operation = request.form.get("operation")

        if operation == "sum":
            result = var1 + var2

        elif operation == "sub":
            result = var1 - var2

        elif operation == "mul":
            result = var1 * var2

        elif operation == "div":
            if var2 == 0:
                result = "Cannot divide by zero"
            else:
                result = var1 / var2

    return render_template("Calculate1.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)