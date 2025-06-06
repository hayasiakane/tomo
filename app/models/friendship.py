from app.extensions import db
from datetime import datetime

class friendships(db.Model):
    """好友关系模型"""
    __tablename__ = 'friendships'
    friendship_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('User.userId'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('User.userId'), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)