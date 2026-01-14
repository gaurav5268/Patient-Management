import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "patients.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        gender TEXT,
        city TEXT,
        height REAL,
        weight REAL,
        status TEXT,
        mobile TEXT,
        symptoms TEXT
    )
    """)

    conn.commit()
    conn.close()
