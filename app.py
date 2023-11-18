from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

counter = 0

@app.route("/")
def home():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM currencies WHERE charcode NOT LIKE 'RUB' ORDER BY name")

    rows = cur.fetchall()
    con.close()

    return render_template("index.html", rows=rows)


@app.route("/button", methods = ['POST', 'GET'])
def button():
    if request.method == 'POST':
        global counter
        counter += 1
    return render_template("button.html", counter=counter)

@app.route("/convert")
def convert():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM currencies ORDER BY name")

    rows = cur.fetchall()
    con.close()
   
    return render_template("converter.html", rows=rows)

@app.route("/convert_result", methods = ['POST', 'GET'])
def convert_result():
    if request.method == 'POST':
        try:
            cur1 = request.form['cur1']
            cur2 = request.form['cur2']
            amount = int(request.form['amount'])
        finally:
            # TODO: refactor this into business logic layer

            con = sqlite3.connect("database.db")
            #con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute(f"SELECT rate FROM currencies WHERE name = '{cur1}'")
            cur1rate = cur.fetchone()[0]

            cur = con.cursor()
            cur.execute(f"SELECT rate FROM currencies WHERE name = '{cur2}'")
            cur2rate = cur.fetchone()[0]
            
            con.close()


            result = 0
            if cur2 == "Российский рубль":
                result = cur1rate * amount 
            elif cur1 == "Российский рубль":
                result = 1.0 / cur2rate * amount
            else:
                result = cur1rate / cur2rate * amount

            msg = f"Перевод из {cur1} в количестве {amount} в {cur2}. Результат: {result}"

            return render_template("convert_result.html",msg=msg)
