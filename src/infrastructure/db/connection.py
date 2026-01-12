import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

DB_PATH = BASE_DIR / "data" / "troco_do_troco.db"

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
