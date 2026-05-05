import sys
import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "nightwatch.db"

def add_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email.strip().lower(), generate_password_hash(password))
        )
        conn.commit()
        print(f"User {email} created successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: {email} already exists in the database.")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/add_user.py email@example.com yourpassword")
        sys.exit(1)
    add_user(sys.argv[1], sys.argv[2])