from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from .models import User
from .database import get_db
from . import mail

auth = Blueprint("auth", __name__)

def get_serializer():
    return URLSafeTimedSerializer(current_app.secret_key)

def send_confirmation_email(email):
    token = get_serializer().dumps(email, salt="email-confirm")
    confirm_url = url_for("auth.confirm_email", token=token, _external=True)
    msg =Message(
        subject="Confirm your Nightwatch account",
        recipients=[email],
        body=f"Click the link below to confirm your account. The link expires in 24 hours.\n\n{confirm_url}\n\nIf you did not register for Nightwatch, ignore this email."
    )
    mail.send(msg)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.get_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            if not user.is_active:
                flash("Please confirm your email address before logging in.")
                return render_template("login.html")
            login_user(user)
            return redirect(url_for("main.index"))
        flash("Invalid email or password.")
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if password != confirm:
            flash("Passwords do not match.")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return render_template("register.html")

        conn = get_db()

        # check whitelist
        whitelisted = conn.execute(
            "SELECT id FROM email_whitelist WHERE email = ?",
            (email,)
        ).fetchone()

        if not whitelisted:
            conn.close()
            flash("That email address is not authorised to register.")
            return render_template("register.html")

        # check not already registered
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if existing:
            conn.close()
            flash("An account with that email already exists.")
            return render_template("register.html")

        # create the user
        conn.execute(
            "INSERT INTO users (email, password_hash, is_active) VALUES (?, ?, 0)",
            (email, generate_password_hash(password))
        )
        conn.commit()
        conn.close()

        try:
            send_confirmation_email(email)
            flash("Account created.Check your email for a confirmation link.")
        except Exception as e:
            current_app.logger.error(f"Mail error: {e}")
            flash("Account created but confirmation email faild to send. Contact an admin")       
            return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth.route("/confirm/<token>")
def confirm_email(token):
    try:
        email = get_serializer().loads(token, salt="email-confirm", max_age=86400)
    except SignatureExpired:
        flash("The confirmation link has expired. Please refister again.")
        return redirect(url_for("auth.register"))
    except BadSignature:
        flash("Invalid confirmation link.")
        return redirect(url_for("auth.login"))

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?",(email,)
    ).fetchone()

    if not user:
        conn.close()
        flash("Account not found.")
        return redirect(url_for("auth.register"))

    if user["is_active"]:
        conn.close()
        flash("Account already confirmed. You can log in.")
        return redirect(url_for("auth.login"))

    conn.execute(
        "UPDATE users SET is_active = 1 WHERE email = ?", (email,)
    )
    conn.commit()
    conn.close()

    flash("Email confirmed. You can now log in.")
    return redirect(url_for("auth.login"))
    