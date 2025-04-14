import sqlite3

conn = sqlite3.connect('data.db')

# Create the main list table
conn.execute('CREATE TABLE IF NOT EXISTS list (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, count INTEGER, description TEXT)')

# Create the history table
conn.execute('''
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        count INTEGER,
        description TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Add an index to the `item` column in the `history` table
conn.execute('CREATE INDEX IF NOT EXISTS idx_history_item ON history (item)')

conn.commit()
conn.close()
