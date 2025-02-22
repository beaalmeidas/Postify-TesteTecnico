from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db_config import DBConfig


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DBConfig)

    db.init_app(app)

    return app