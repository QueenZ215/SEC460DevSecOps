from flask_login import UserMixin
from .database import get_db

class User(UserMixin):
    def __init__(self, id, email, password_hash):
        self.id = id
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def get_by_id(user_id):
        conn = get_db()
        row = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        conn.close()
        if row:
            return User(row["id"], row["email"], row["password_hash"])
        return None

    @staticmethod
    def get_by_email(email):
        conn = get_db()
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        conn.close()
        if row:
            return User(row["id"], row["email"], row["password_hash"])
        return None