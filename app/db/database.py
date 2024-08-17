import sqlite3

conn = sqlite3.connect('fastapi.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT NOT NULL
)
''')

cursor.execute('''
INSERT INTO users (name, email, password)
VALUES ('admin','admin_email@example.com', 'password')
''')

conn.commit()
conn.close()
