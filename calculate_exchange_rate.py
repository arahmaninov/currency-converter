import sqlite3

def calculate(currency1, currency2, amount):
    con = sqlite3.connect("database.db")
    
    cur = con.cursor()
    cur.execute(f"SELECT rate FROM currencies WHERE name = '{currency1}'") 
    currency_1_rate = cur.fetchone()[0]

    cur = con.cursor()
    cur.execute(f"SELECT rate FROM currencies WHERE name = '{currency2}'")
    currency_2_rate = cur.fetchone()[0]

    con.close()

    result = 0

    if currency2 == "Российский рубль":
        result = currency_1_rate * amount
    elif currency1 == "Российский рубль":
        result = 1.0 / currency_2_rate * amount
    else:
        result = currency_1_rate / currency_2_rate * amount

    result = round(result, 5)

    return result

