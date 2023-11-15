import xml.etree.ElementTree as ET
import urllib.request
import sqlite3

# Creating database
conn = sqlite3.connect('database.db')
print("Connected to database successfully")
cur = conn.cursor()
cur.execute('DROP TABLE currencies') # clear the table
cur.execute('CREATE TABLE currencies (numcode INTEGER, charcode TEXT, name TEXT, rate REAL)')

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
    numcode = currency.find('NumCode').text
    charcode = currency.find('CharCode').text
    name = currency.find('Name').text
    torub = currency.find('VunitRate').text
    print(f"Цифр. код валюты: {numcode} Букв. код валюты: {charcode} Название: {name} Курс: {torub}")

    try:
        with sqlite3.connect('database.db') as con:
            current = con.cursor()
            current.execute("INSERT INTO currencies (numcode, charcode, name, rate) VALUES (?, ?, ?, ?)", (int(numcode), charcode, name, float(torub.replace(',', '.'))))
            con.commit()
            print("Record successfully added to the database")
    except:
        con.rollback()
        print("ERROR in the INSERT")

    currency_counter += 1

print(f"\nВсего {currency_counter} валют")
