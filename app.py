from flask import Flask 
import pandas as pd
from flask import Flask, request, render_template 
import sqlite3
import ccxt 
from datetime import date
app = Flask(__name__)



global connection
connection = sqlite3.connect('trades.db')
global cur
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS trades(id INTEGER PRIMARY KEY AUTOINCREMENT, coin TEXT, amount FLOAT, entry FLOAT, date TEXT)") 
def main():
    coin = str(input("What is coin? "))
    amount = float(input("How many? "))
    entry = float(input("What price? "))
    today = date.today()
    datenow = today.strftime("%b-%d-%Y")
 
    sql_insert(coin, amount, entry, datenow)
    coin_info(coin)


def coin_info(coin):

    rows = cursor.execute("SELECT id, coin, amount, entry, date FROM trades").fetchall() 
    print(rows)

def sql_insert(coin, amount, entry, newdate):
    # --------- # 
    # Checks for existing value in the database 
    # If it is not, then add value to the database
    # If it is, then retrieve values, drop the table
    # Then add it to the database
    # For variable amount -> ( amount + amount ) = new amount
    # For variable entry -> (entry + entry / 2) = new entry or averaged entry

    today = date.today()
    datenow = today.strftime("%b-%d-%Y")
    check_for_existing = cursor.execute("SELECT id, coin FROM trades WHERE coin  = '{0}'".format(coin)).fetchone()

    if check_for_existing == None:
        insert = 'INSERT INTO trades(coin, amount, entry, date) VALUES("{0}", {1}, {2}, "{3}")'.format(coin, float(amount), float(entry), datenow)
        cursor.execute(insert) 
        connection.commit()
    else:
        existing_value =  cursor.execute("SELECT coin, amount, entry  FROM trades WHERE coin = '{0}'".format(coin)).fetchone()
        amount = amount + existing_value[1]
        entry = (entry + existing_value[2]) / 2
        if newdate == datenow:
            pass
        else:
            newdate = newdate + ' | ' + datenow 

        print('EXISTING VALUE', existing_value, amount, entry, newdate)

        connection.commit()
        # Drop a row then add new table. 
        # OR 
        # Update table with unique ID.
main()
#
#@app.route("/")
#
#def main():
#    while True:
#        return render_template('home.html')
#
#

