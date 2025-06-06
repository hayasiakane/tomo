from app.extensions import db
from datetime import datetime

class Restaurant(db.Model):
    """餐厅模型"""
    __tablename__ = 'Restaurant'
    restaurantId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    cuisine = db.Column(db.String(100))
    description = db.Column(db.Text)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    userId = db.Column(db.Integer, db.ForeignKey('User.userId'), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    review_count = db.Column(db.Integer, nullable=True, default=0)
    average_rating = db.Column(db.Float, nullable=True, default=0.0)
    phone = db.Column(db.String(20), nullable=False)
    website = db.Column(db.String(255), nullable=False)


class restaurant_images(db.Model):
    """餐厅图片模型"""
    __tablename__ = 'restaurant_images'
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurantId = db.Column(db.Integer, db.ForeignKey('Restaurant.restaurantId'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
 