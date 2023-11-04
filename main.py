import requests
from flask import Flask, render_template, request
import locale


def get_rates():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    response.raise_for_status()
    _data = response.json()
    return _data


data = get_rates()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def currency_calculator():
    result = None
    if request.method == "POST":
        selected_currency = request.form['currency']
        amount = float(request.form['amount'])
        for rate in data[0]['rates']:
            if rate['code'] == selected_currency:
                exchange_rate = rate['ask']
                result = amount * exchange_rate
                break  # Stop searching when you find the selected currency

        formatted_result = locale.currency(result, grouping=True)

        return render_template('calculator.html', data=data, result=formatted_result,
                               selected_currency=selected_currency)

    return render_template("calculator.html", data=data)


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'pl_PL.utf8')  # Polish locale
    app.run(debug=True)
    # print(data)

