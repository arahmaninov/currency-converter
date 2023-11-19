import xml.etree.ElementTree as ET
import urllib.request
import sqlite3

def fetch():
    # Creating database
    conn = sqlite3.connect('database.db')
    print("Connected to database successfully")
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS currencies') # clear the table
    cur.execute('CREATE TABLE currencies (charcode TEXT, name TEXT, rate REAL)')

    conn.close()

    # Getting XML
    print("Getting XML file https://cbr.ru/scripts/XML_daily.asp ...")
    url = 'https://cbr.ru/scripts/XML_daily.asp'
    response = urllib.request.urlopen(url).read()

    root = ET.fromstring(response)

    print(f"Курс валют к рублю, установленный ЦБ РФ на {root.attrib['Date']}")

    print()

    # Filling in the database
    currency_counter = 0
    for currency in root.findall('Valute'):
        charcode = currency.find('CharCode').text
        name = currency.find('Name').text
        torub = currency.find('VunitRate').text
        print(f"Букв. код валюты: {charcode} Название: {name} Курс: {torub}")

        try:
            with sqlite3.connect('database.db') as con:
                current = con.cursor()
                current.execute("INSERT INTO currencies (charcode, name, rate) VALUES (?, ?, ?)", (charcode, name, float(torub.replace(',', '.'))))
                con.commit()
                print("Record successfully added to the database")
        except:
            con.rollback()
            print("ERROR in the INSERT")

        currency_counter += 1
        
    # add RUB for conversion purposes
    try:
        with sqlite3.connect('database.db') as con:
            current = con.cursor()
            current.execute("INSERT INTO currencies (charcode, name, rate) VALUES (?, ?, ?)", ("RUB", "Российский рубль", 1))
            con.commit()
            print("RUB successfully added to the database")
    except:
        con.rollback()
        print("ERROR in the INSERT RUB")

    print(f"\nВсего {currency_counter} валют")
