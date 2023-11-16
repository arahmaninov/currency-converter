from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM currencies ORDER BY name")

    rows = cur.fetchall()
    con.close()

    return render_template("index.html", rows=rows)

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
            msg = f"Перевод из {cur1} в {cur2} в количестве {amount}"
            return render_template("convert_result.html",msg=msg)
