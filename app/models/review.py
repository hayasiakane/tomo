from app.extensions import db
from datetime import datetime

class review(db.Model):
    """评价模型"""
    __tablename__ = 'review'
    reviewId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('User.userId'), nullable=False)
    restaurantId = db.Column(db.Integer, db.ForeignKey('Restaurant.restaurantId'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.SmallInteger, nullable=False)
    pin = db.Column(db.Boolean, default=False)
    like = db.Column(db.Integer, default=0)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
