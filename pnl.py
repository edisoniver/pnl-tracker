import ccxt
import sqlite3


connection = sqlite3.connect("trades.db")

cursor = connection.cursor()

cursor.execute("CREATE TABLE trades (coin TEXT, amount INTEGER, average_price INTEGER)") 

cursor.execute("INSERT INTO trades VALUES('ZEC', 2, 400)")

cursor.execute("INSERT INTO trades VALUES('ADA', 1.2, 4500)")


rows = cursor.execute("SELECT coin, amount, average_price FROM trades").fetchall() 

connection.commit()
print(rows)

# Create functions that insert data into the database and display it into a Flask Web app. 

# Finds matching coin, finds API and displays price in real time. 

