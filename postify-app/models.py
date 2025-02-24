from .db_config import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone


# MODEL DE USUÁRIO
class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password_hash = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def secure_password(self, user_password):
        self.user_password_hash = generate_password_hash(user_password)

    def check_password(self, user_password):
        return check_password_hash(self.user_password_hash, user_password)
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_email': self.user_email,
            'username': self.username,
            'is_admin': self.is_admin
        }
    
    def get_id(self):
        return str(self.user_id)


# MODEL DE POSTAGEM
class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('authored_posts', lazy=True))

    def to_dict(self):
        return {
            'post_id': self.post_id,
            'user_id': self.user_id,
            'post_content': self.post_content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user': self.user.username if self.user else None
        }
    
    def get_id(self):
        return str(self.post_id)