from flask import Flask, render_template
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
