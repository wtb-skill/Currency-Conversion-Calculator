import requests
from flask import Flask, render_template, request, send_file
import csv
import io
from typing import Any, List, Dict

app = Flask(__name__)


def get_rates() -> List[Dict[str, Any]]:
    """
    Fetches currency exchange rate data from NBP API.

    :return: List[Dict[str, Any]]: A list of dictionaries containing currency exchange rate data.
    """
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    response.raise_for_status()
    _data = response.json()
    return _data


def create_csv(data: List[Dict[str, Any]]) -> Any:
    """
    Creates a CSV file with currency exchange rate data.

    :param data: (List[Dict[str, Any]]): List of dictionaries containing currency exchange rate data.
    :return: Any: A CSV file as an attachment.
    """
    with io.StringIO() as output:
        writer = csv.writer(output)

        # Write the CSV header
        writer.writerow(['Currency', 'Code', 'Bid', 'Ask'])

        for row in data[0]['rates']:
            writer.writerow([row['currency'], row['code'], row['bid'], row['ask']])

        output.seek(0)  # Reset the file pointer to the beginning
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            as_attachment=True,
            download_name='exchange_rates.csv',
            mimetype='text/csv'
        )


@app.route('/download_csv', methods=['GET'])
def download_csv() -> Any:
    """
    Endpoint for downloading the CSV file of currency exchange rates.

    :return: Any: A CSV file as an attachment.
    """
    data = get_rates()  # Fetch fresh data from the API
    return create_csv(data)


@app.route('/display_rates')
def display_csv_data() -> str:
    """
    Displays currency exchange rate data.

    :return: str: Rendered HTML page.
    """
    data = get_rates()  # Fetch fresh data from the API
    date = data[0]['effectiveDate']

    return render_template('exchange_rates.html', data=data[0]['rates'], date=date)


@app.route("/calculator", methods=["GET", "POST"])
def currency_calculator() -> str:
    """
    Currency conversion calculator.

    :return: str: Rendered HTML page.
    """
    result = None
    data = get_rates()  # Fetch fresh data from the API
    date = data[0]['effectiveDate']

    if request.method == "POST":
        selected_currency = request.form['currency']
        amount = float(request.form['amount'])
        for rate in data[0]['rates']:
            if rate['code'] == selected_currency:
                exchange_rate = rate['ask']
                result = amount * exchange_rate
                break  # Stop searching when you find the selected currency

        formatted_amount = '{:,.2f}'.format(amount)
        rounded_result = round(result, 2)
        formatted_result = '{:,.2f}'.format(rounded_result)
        message = f"The exchange of {formatted_amount} {selected_currency} requires {formatted_result} PLN."

        return render_template('calculator.html', data=data, date=date, message=message)

    return render_template("calculator.html", data=data, date=date)


if __name__ == '__main__':
    app.run(debug=True)

