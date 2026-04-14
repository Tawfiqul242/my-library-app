import sqlite3

def connect():
    return sqlite3.connect("library.db")

def create_table():
    conn = connect()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()