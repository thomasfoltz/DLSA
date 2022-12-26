import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cursor=connection.cursor()
cursor.execute("INSERT INTO stocks (ticker, quantity) VALUES (?, ?)", ("MSFT", 1))

connection.commit()
connection.close()