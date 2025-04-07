import sqlite3

DB_FILE = "url_shortener.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_url TEXT UNIQUE NOT NULL,
                expiration_date TEXT NOT NULL
            )
        """)
        conn.commit()

def insert_url(original_url: str, short_url: str, expiration_date: str):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (original_url, short_url, expiration_date) VALUES (?, ?, ?)",
                       (original_url, short_url, expiration_date))
        conn.commit()

def fetch_url_by_short(short_url: str):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_url, expiration_date FROM urls WHERE short_url = ?", (short_url,))
        return cursor.fetchone()
