import sqlite3

# Connect or create signals.db
conn = sqlite3.connect('signals.db')
cursor = conn.cursor()

# Create signals table (if not exists)
cursor.execute('''
CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    signal TEXT NOT NULL,
    amount REAL NOT NULL,
    last_updated TEXT NOT NULL
)
''')

conn.commit()
conn.close()
print("signals.db तैयार हो गया ✅")
