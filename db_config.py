import os
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class DBConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:1234@localhost/postify_db'