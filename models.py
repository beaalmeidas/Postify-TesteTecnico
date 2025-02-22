from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password_hash = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def secure_password(self, user_password):
        self.user_password_hash = generate_password_hash(user_password)

    def check_password(self, user_password):
        return check_password_hash(self.user_password_hash, user_password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.timezone.utc)
    updated_at = db.Column(db.DateTime, default=datetime.timezone.utc, onupdate=datetime.timezone.utc)

    user = db.relationship('User', backref=db.backref('authored_posts', lazy=True))