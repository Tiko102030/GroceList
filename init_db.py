import sqlite3

conn = sqlite3.connect('data.db')
conn.execute('CREATE TABLE IF NOT EXISTS list (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT)')
conn.commit()
conn.close()
