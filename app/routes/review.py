from flask import Blueprint, request, jsonify
from app.models.review import Review
from app.utils.decorators import login_required

review_bp = Blueprint('review', __name__)

@review_bp.route('/api/restaurants/<restaurant_id>/reviews', methods=['POST'])
@login_required
def api_add_review(restaurant_id):
    user_id = request.cookies.get('user_id')
    data = request.get_json()
    
    review_id, error = Review.create(
        user_id=user_id,
        restaurant_id=restaurant_id,
        content=data.get('content'),
        rating=data.get('rating')
    )
    
    if error:
        return {'error': error}, 400
    
    return {'reviewId': review_id}, 201

@review_bp.route('/api/restaurants/<restaurant_id>/reviews', methods=['GET'])
def api_get_reviews(restaurant_id):
    reviews, error = Review.get_by_restaurant(restaurant_id)
    if error:
        return {'error': error}, 400
    
    return {'reviews': reviews}