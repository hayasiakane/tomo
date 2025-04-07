from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.restaurant import Restaurant
from app.utils.decorators import login_required, business_account_required

restaurant_bp = Blueprint('restaurant', __name__)

@restaurant_bp.route('/api/restaurants', methods=['POST'])
@login_required
@business_account_required
def api_add_restaurant():
    user_id = request.cookies.get('user_id')
    data = request.get_json()
    
    restaurant_id, error = Restaurant.create(
        owner_id=user_id,
        name=data.get('name'),
        address=data.get('address'),
        cuisine=data.get('cuisine', ''),
        description=data.get('description', '')
    )
    
    if error:
        return {'error': error}, 400
    
    return {'restaurantId': restaurant_id}, 201

@restaurant_bp.route('/api/restaurants/<restaurant_id>', methods=['GET'])
def api_get_restaurant(restaurant_id):
    restaurant, error = Restaurant.get_by_id(restaurant_id)
    if error:
        return {'error': error}, 404
    
    return restaurant