from flask_login import UserMixin
from .database import get_db

class User(UserMixin):
    def __init__(self, id, email, password_hash, is_active=0):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self._is_active = is_active

    @property
    def is_active(self):
        return bool(self._is_active)

    @staticmethod
    def get_by_id(user_id):
        conn = get_db()
        row = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        conn.close()
        if row:
            return User(row["id"], row ["email"], row["password_hash"], row["is_active"])
        return None    

    @staticmethod
    def get_by_email(email):
        conn = get_db()
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        conn.close()
        if row:
            return User(row["id"], row["email"], row["password_hash"], row["is_active"])
        return None