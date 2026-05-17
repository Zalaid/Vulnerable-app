"""
session.py
Manages SQLite database connections and schema initialization for the application.
"""
import sqlite3
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
DB_PATH = os.path.join(_PROJECT_ROOT, 'vulnerable_app.db')


def get_db():
    """Open and return a configured SQLite database connection."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the application database schema if it does not already exist."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email    TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()
