import sqlite3

DB_PATH = "nightwatch.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cves (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            cve_id        TEXT UNIQUE,
            description   TEXT,
            cvss_score    REAL,
            severity      TEXT,
            published     TEXT,
            last_modified TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            email         TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_active     INTEGER DEFAULT 0,
            created_at    TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS email_whitelist (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            email     TEXT UNIQUE NOT NULL,
            added_at  TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS user_keywords (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        keyword TEXT NOT NULL,
        UNIQUE(user_id, keyword),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
""")

    try:
        conn.execute("ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 0")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # column already exists, that's fine
    conn.commit()
    conn.close()