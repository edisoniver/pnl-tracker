from flask import Flask 
import pandas as pd
from flask import Flask, request, render_template 
import sqlite3
import ccxt 
import pandas as pd
import sqlalchemy as sqla
from datetime import date
app = Flask(__name__)

exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': 'FboyssPKoBtfkOgCW7YQPzKxOCrRW3ZZTyUYC3JjfIgUV3S5cQxjSoqSA1uqXu8F',
    'secret': 'zEe3pMmuO3OqovIZOpYb20QWGiudJg5tJ1SIZ8fKPAnzMYj2r5r2R18VgBIQQYbk',
    'timeout': 30000,
    'enableRateLimit': True,
})

    # Repeat this for all symbols in database and display it onto the Flask Website. 

    #print(test['lastPrice'])





global connection
connection = sqlite3.connect('trades.db')
global cur
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS trades(id INTEGER PRIMARY KEY AUTOINCREMENT, coin TEXT, amount FLOAT, date TEXT)") 

@app.route("/")

def main():
    return render_template('home.html')




def starter():
 
 #   print(get_coin_values())
   # balance = fetches_balance_amount()
   # coins = get_coin_values()
   # print(coins[1], balance, coins[0])
   # fetch_account()
   panda_dataframe()


def panda_dataframe():
    db = sqla.create_engine('sqlite:///trades.db')
    datas=pd.read_sql('SELECT * FROM trades', db)
    print(datas)



def sql_insert(coin, amount, newdate):
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
        insert = 'INSERT INTO trades(coin, amount, date) VALUES("{0}", {1}, "{2}")'.format(coin, float(amount), datenow)
        cursor.execute(insert) 
        connection.commit()
    else:
        existing_value =  cursor.execute("SELECT coin, amount FROM trades WHERE coin = '{0}'".format(coin)).fetchone()
        amount = amount + existing_value[1]
        #entry = (entry + existing_value[2]) / 2
        if newdate == datenow:
            pass
        else:
            newdate = newdate + ' | ' + datenow 
        variable = 'UPDATE trades SET amount = {0} WHERE coin = "{2}"'.format(float(amount), coin)  
        update = cursor.execute(variable)        
        
        connection.commit()

def get_coin_values():
   # ----------------------- # 
   # need to fetch data from Binance API and input it into the SQL database. 
   # We need coin name, price, amount and date. 
   # We need to fetch this every x seconds. j
    coins = cursor.execute("SELECT coin from TRADES").fetchall() 
    coin_stripped = []
    for x in coins:
        coin_stripped.append(x)
    new_strip = [] # This is the resultant array of the coins in the database. Cleaned and ready to go :)))

    for i in coin_stripped:
        x = str(i)
        g = x.strip("(),'")
        new_strip.append(g)
    # Get an array that gets prices with the coins. 
    # 1. Get coin -> get price ticker -> get price -> place into array
    new_strip.remove('USDT')
    new_strip.remove('QI')
    new_strip.remove('NSBT')
    price_of_the_coin = []
    for items in new_strip:
        x = fetches_coin_price(items)
        price_of_the_coin.append(x)


    return [price_of_the_coin, new_strip]
def fetches_balance_amount(): # Fetches the amount of coins in the balance.
    balance = []
    amount = cursor.execute("SELECT amount FROM trades").fetchall()
    for x in amount:
        x = str(x)
        x = x.strip('(),')
        balance.append(x)

    
    return balance

def fetches_coin_price(coins):
    try:
        if (exchange.has['fetchTicker']):
            coin_pair = '{0}/USDT'.format(coins)
            get_price = exchange.fetch_ticker(coin_pair)
           # print(get_price['info']['lastPrice'])
            coin_price = get_price['info']['lastPrice']     
    except:
        if (exchange.has['fetchTicker']):
            coin_pair = '{0}/BTC'.format(coins)
            get_price = exchange.fetch_ticker(coin_pair)
           # print(get_price['info']['lastPrice'])
            coin_price = get_price['info']['lastPrice']
    return coin_price





def fetch_account():
    # Fetches account balance
    #print (exchange.fetch_balance())
    data = exchange.fetch_balance()
    my_balance = data["total"]
    today = date.today()
    datenow = today.strftime("%b-%d-%Y")

    # Data prints out a dictionary. Make a loop of all values that are not empty and add them to the SQL database. 

    coin_balance = []

    # This initializes the account. 
    for coins, price in my_balance.items():
        if price == 0.0:
            pass
        else:
            coin_balance.append([coins, price])
    for items in coin_balance:

        check_for_existing = cursor.execute("SELECT id, coin FROM trades WHERE coin  = '{0}'".format(items[0])).fetchone()
        if check_for_existing == None:
            command = 'INSERT INTO trades(coin, amount, date) VALUES("{0}", {1}, "{2}")'.format(items[0], float(items[1]), datenow)
            cursor.execute(command)
            connection.commit()
        else:
            variable = 'UPDATE trades SET amount = {0} WHERE coin = "{1}"'.format(float(items[1]), items[0])
            cursor.execute(variable)
            connection.commit()
        
starter()

if __name__ == "__main__":
        app.run()
