import sqlite3

connection = sqlite3.connect('instance/app.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (

               id INTEGER PRIMARY KEY AUTOINCREMENT,
               review_text TEXT NOT NULL,
               sentiment TEXT NOT NULL           
    )
""")

connection.commit()
connection.close()