import random
from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    secret_number = request.cookies.get("secret_number")  # check if there is already a cookie named secret_number

    response = make_response(render_template("index.html"))
    if not secret_number:  # if not, create a new cookie
        new_secret = random.randint(1, 10)
        response.set_cookie("secret_number", str(new_secret))

    return response


@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))
    secret_number = int(request.cookies.get("secret_number"))

    if guess == secret_number:
        message = "Du bist Hellseher! Die geheime Zahl ist {0}".format(str(secret_number))
        response = make_response(render_template("result.html", message=message))
        response.set_cookie("secret_number", str(random.randint(1, 10)))  # set the new secret number
        return response
    elif guess > secret_number:
        message = "Noch nicht ganz ... probier eine kleinere Zahl."
        return render_template("result.html", message=message)
    elif guess < secret_number:
        message = "Du hast es fast ... probier eine größere Zahl."
        return render_template("result.html", message=message)


if __name__ == '__main__':
    app.run(debug=True)  # if you use the port parameter, delete it before deploying to Heroku