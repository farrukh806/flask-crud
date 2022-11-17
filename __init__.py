from flask import Flask
import os
from flask_login import LoginManager, current_user
from .blueprints.auth import auth
from .blueprints.main import main
from .extensions import db
from .models.person import Person


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DB_URL') or 'postgresql://postgres:postgres@localhost/postgres'
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.do_login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Person.query.get(int(id))

    app.register_blueprint(auth)
    app.register_blueprint(main)
    return app
