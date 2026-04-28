from flask import Flask
from .database import init_db
import os

def create_app():
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(__file__), "templates"))
    init_db()
    from .routes import main
    app.register_blueprint(main)
    return app