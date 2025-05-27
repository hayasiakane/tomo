from flask import jsonify,Blueprint, render_template, request, redirect, url_for, flash
from app.models.restaurant import Restaurant
from app.utils.decorators import login_required, business_account_required
from gremlin_python.driver import client  # 添加这行

restaurant_bp = Blueprint('restaurant', __name__)

@restaurant_bp.route('/api/restaurants', methods=['POST'])
# @login_required
# @business_account_required
def api_add_restaurant():
    user_id = request.headers.get('X-User-ID')
    data = request.get_json()
    
    try:
        # 初始化Gremlin连接
        gremlin_client = client.Client('ws://localhost:8182/gremlin', 'g')
        
        restaurant_id, error = Restaurant.create(
            owner_id=user_id,
            name=data.get('name'),
            address=data.get('address'),
            cuisine=data.get('cuisine', ''),
            description=data.get('description', '')
        )

        restaurants_data, error = Restaurant.get_by_id(restaurant_id)  
        if error:
            return {'error': error}, 400
        return jsonify({
            "message": "Registration successful",
            "restaurantId": restaurants_data['restaurantId'],
            "name": restaurants_data['name'],
            "address": restaurants_data['address'],
            'cuisine': restaurants_data.get('cuisine', [''])
            #"token": "模拟Token",  # 生产环境替换为真实JWT
        }), 201

    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'gremlin_client' in locals():
            gremlin_client.close()
    
    #return {'restaurantId': restaurant_id}, 201


@restaurant_bp.route('/api/restaurants', methods=['GET'])
def api_get_all_restaurants():
    search = request.args.get('search', '')
    cuisine = request.args.get('cuisine', '')
    
    restaurants_data, error = Restaurant.get_all(search=search, cuisine=cuisine)
    if error:
        return {'error': error}, 500
    else:
        print("Restaurant found:", restaurants_data)
    
    total_pages = 1  # 暂时简化处理，不分页
    return {
        'restaurants': restaurants_data['restaurants'],
        'totalPages': total_pages
    }, 200


@restaurant_bp.route('/api/restaurants/<restaurant_id>', methods=['GET'])
def api_get_restaurant(restaurant_id):
    restaurant, error = Restaurant.get_by_id(restaurant_id)
    if error:
        return {'error': error}, 404
    
    return restaurant

@restaurant_bp.route('/restaurants/<restaurant_id>')
def restaurant_detail(restaurant_id):
    restaurant, error = Restaurant.get_by_id(restaurant_id)
    if error:
        return {'error': error}, 404
    
    return render_template('restaurant/detail.html', restaurant=restaurant)