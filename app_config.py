from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db_config import DBConfig
from flask_login import LoginManager
from .models import User


db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


def create_app():
    app = Flask(__name__)
    app.config.from_object(DBConfig)

    db.init_app(app)
    login_manager.init_app(app)

    return app