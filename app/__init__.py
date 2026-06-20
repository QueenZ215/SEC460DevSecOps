import os
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from .database import init_db
from .models import User

mail = Mail()

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-only-change-me")
    # mail config
    app.config["MAIL_SERVER"]          = os.getenv("MAIL_SERVER", "smtp.mailbox.org")
    app.config["MAIL_PORT"]            = int(os.getenv("MAIL_PORT", 465))
    app.config["MAIL_USE_TLS"]         = False
    app.config["MAIL_USE_SSL"]         = True
    app.config["MAIL_USERNAME"]        = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"]        = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"]  = os.getenv("MAIL_DEFAULT_SENDER")

    mail.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(int(user_id))

    init_db()

    from .routes import main
    from .auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    @app.after_request
    def set_security_headers(response):
        response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'; form-action 'self'"
        return response

    return app