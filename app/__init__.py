import os
from flask import Flask
from flask_login import LoginManager
from .database import init_db
from .models import User

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-only-change-me")

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

    return app