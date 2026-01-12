from infrastructure.db.connection import get_connection
from pathlib import Path

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    schema_path = Path(__file__).resolve().parents[1] / "infrastructure" / "db" / "schema.sql"

    with open(schema_path) as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized")
