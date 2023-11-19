from flask import Flask, render_template, request
import sqlite3
import fetch_currency_rates, calculate_exchange_rate 

app = Flask(__name__)

fetch_currency_rates.fetch() # getting rates and filling db

# currency rates to RUB on current date
@app.route("/rates")
def home():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM currencies WHERE charcode NOT LIKE 'RUB' ORDER BY name")

    rows = cur.fetchall()
    con.close()

    return render_template("index.html", rows=rows)

# currency conversion form
@app.route("/convert")
def convert():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM currencies ORDER BY name")

    rows = cur.fetchall()
    con.close()
   
    return render_template("converter.html", rows=rows)

# calculate currency conversion
@app.route("/convert_result", methods = ['POST', 'GET'])
def convert_result():
    if request.method == 'POST':
        try:
            currency1 = request.form['cur1']
            currency2 = request.form['cur2']
            amount = int(request.form['amount'])
        finally:
            result = calculate_exchange_rate.calculate(currency1, currency2, amount)

            msg = f"Перевод из {currency1} в количестве {amount} в {currency2}. Результат: {result}"

            return render_template("convert_result.html",msg=msg)
