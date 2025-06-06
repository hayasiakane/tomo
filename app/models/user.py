from app.extensions import db
from datetime import datetime

class User(db.Model):
    """用户模型"""
    __tablename__ = 'User'
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255))
    type = db.Column(db.String(10), default='regular')  # Default type is 'regular'
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
