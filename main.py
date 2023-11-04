import requests
from flask import Flask, render_template, request


def get_rates():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    response.raise_for_status()
    data = response.json()
    return data


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def book_manager():
    # if request.method == "POST":
    #     data = request.form
    #     title = data.get('title')
    #     author = data.get("author")
    #     release_date = data.get('release_date')
    #     comment = data.get("comment")



    return render_template("calculator.html")


if __name__ == '__main__':
    app.run(debug=True)

