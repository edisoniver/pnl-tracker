from flask import Flask 
import pandas as pd
from flask import Flask, request, render_template 
import sqlite3
import ccxt 
app = Flask(__name__)



global connection
connection = sqlite3.connect('trades.db')
global cur
cursor = connection.cursor()

def main():
    coin = str(input("What is coin"))
    amount = float(input("How much"))
    entry = float(input("What price"))
    
    sql_insert(coin, amount, entry)
    coin_info(coin)


def coin_info(coin):

    rows = cursor.execute("SELECT coin, amount, entry FROM trades").fetchall() 
    print(rows)

def sql_insert(coin, amount, entry):
    
    insert = 'INSERT INTO trades VALUES("{0}", {1}, {2})'.format(coin, float(amount), float(entry))

    cursor.execute(insert) 
    connection.commit()

main()
#
#@app.route("/")
#
#def main():
#    while True:
#        return render_template('home.html')
#
#

