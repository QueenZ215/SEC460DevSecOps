import sys
import sqlite3

DB_PATH = "nightwatch.db"

def add_to_whitelist(email):
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "INSERT INTO email_whitelist (email) VALUES (?)",
            (email.strip().lower(),)
        )
        conn.commit()
        print(f"{email} added to whitelist.")
    except sqlite3.IntegrityError:
        print(f"Error: {email} is already on the whitelist.")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/add_to_whitelist.py email@example.com")
        sys.exit(1)
    add_to_whitelist(sys.argv[1])