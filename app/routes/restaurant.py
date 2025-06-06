from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.restaurant import Restaurant, restaurant_images
from flask import jsonify
from app.utils.decorators import login_required, business_account_required
from app import db
import os
from werkzeug.utils import secure_filename

restaurant_bp = Blueprint('restaurant', __name__)

@restaurant_bp.route('/add', methods=['POST'])
def api_add_restaurant():
    print("Received request to add restaurant")

    # 获取字段
    user_id = request.form.get('userId')
    name = request.form.get('name')
    address = request.form.get('address')
    cuisine = request.form.get('cuisine')
    description = request.form.get('description')
    phone = request.form.get('phone')
    website = request.form.get('website')

    if not all([user_id, name, address, cuisine]):
        return jsonify({"error": "Missing required fields"}), 400

    # Step 1: 先创建餐厅对象但不含图片路径
    new_restaurant = Restaurant(
        userId=user_id,
        name=name,
        address=address,
        cuisine=cuisine,
        description=description,
        phone=phone,
        website=website,
        image=None  # 暂时为空
    )

    try:
        db.session.add(new_restaurant)
        db.session.commit()

        # Step 2: 获取生成的 restaurantId
        restaurant_id = new_restaurant.restaurantId

        # Step 3: 处理封面图
        cover_image = request.files.get('coverImage')
        if cover_image:
            filename = secure_filename(cover_image.filename)
            upload_folder = os.path.join(current_app.root_path, f'static/restaurant_images/{restaurant_id}')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            cover_image.save(file_path)
            image_path = f"static/restaurant_images/{restaurant_id}/{filename}"

            # 更新图片路径
            new_restaurant.image = image_path
            db.session.commit()  # 提交更新

        return jsonify({
            "message": "Restaurant added successfully",
            "restaurantId": restaurant_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "An error occurred while adding restaurant",
            "error": str(e)
        }), 500



@restaurant_bp.route('/<restaurant_id>', methods=['GET'])
def api_get_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify({
        "restaurantId": restaurant.restaurantId,
        "name": restaurant.name,
        "address": restaurant.address,
        "cuisine": restaurant.cuisine,
        "description": restaurant.description,
        "createdAt": restaurant.createdAt.isoformat(),
        "image": restaurant.image
    }), 200

@restaurant_bp.route('/show/<int:restaurant_id>')
def restaurant_detail(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        flash('Restaurant not found', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('restaurant/detail.html', restaurant=restaurant)

@restaurant_bp.route('/display-all', methods=['GET'])
def api_display_all_restaurants():
    search = request.args.get('search', '').strip()
    cuisine = request.args.get('cuisine', '').strip()

    # 构造查询条件
    query = Restaurant.query

    if search:
        query = query.filter(Restaurant.name.ilike(f"%{search}%"))
    
    if cuisine:
        query = query.filter(Restaurant.cuisine == cuisine)

    # 执行查询
    restaurants = query.all()

    if not restaurants:
        return jsonify({"message": "No restaurants found"}), 404

    # 构造返回数据
    restaurant_list = [{
        "restaurantId": restaurant.restaurantId,
        "name": restaurant.name,
        "address": restaurant.address,
        "cuisine": restaurant.cuisine,
        "description": restaurant.description,
        "createdAt": restaurant.createdAt.isoformat(),
        "image": restaurant.image,
        "review_count": restaurant.review_count,
        "average_rating": restaurant.average_rating
    } for restaurant in restaurants]

    return jsonify({"restaurants": restaurant_list}), 200


@restaurant_bp.route('/my-restaurants/<user_id>', methods=['GET'])
# @login_required
# @business_account_required
def my_restaurants(user_id):
    """  显示当前用户的餐厅列表  """

    # 查询当前用户的餐厅
    restaurants = Restaurant.query.filter_by(userId=user_id).all()
    # 如果没有餐厅，返回空列表
    if not restaurants:
        return jsonify({"message": "No restaurants found for this user"}), 404
    # 构造返回数据
    restaurant_list = [{
        "restaurantId": restaurant.restaurantId,
        "name": restaurant.name,
        "address": restaurant.address,
        "cuisine": restaurant.cuisine,
        "description": restaurant.description,
        "createdAt": restaurant.createdAt.isoformat(),
        "image": restaurant.image,
        "review_count": restaurant.review_count,
        "average_rating": restaurant.average_rating
    } for restaurant in restaurants]

    return jsonify({"restaurants": restaurant_list}), 200

@restaurant_bp.route('/get_images/<restaurant_id>', methods=['GET'])
def get_restaurant_images(restaurant_id):
    """ 获取餐厅的所有图片 """
    images = restaurant_images.query.filter_by(restaurantId=restaurant_id).all()
    if not images:
        return jsonify({"message": "No images found for this restaurant"}), 404
    
    image_list = [{"image_id": img.image_id, "image_path": img.image_path} for img in images]
    
    return jsonify({"images": image_list}), 200

# 上传封面图
@restaurant_bp.route('/upload-image/<int:restaurant_id>', methods=['POST'])
def upload_restaurant_image(restaurant_id):
    """ 上传餐厅封面图 """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if image:
        # 确保目录存在
        save_dir = f'static/restaurant_images/{restaurant_id}'
        os.makedirs(save_dir, exist_ok=True)

        # 安全地保存文件名（防止路径遍历攻击）
        filename = secure_filename(image.filename)
        save_path = os.path.join(save_dir, filename)

        # 保存图片到 static 文件夹
        image.save(save_path)

        # 存储相对路径到数据库（不存储 static/ 前缀）
        relative_path = f'static/restaurant_images/{restaurant_id}/{filename}'

        # 往餐厅模型更新image字段
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        restaurant.image = relative_path
        db.session.commit()

        return jsonify({"message": "Image uploaded successfully", "image_path": relative_path}), 201
    else:
        return jsonify({"error": "Invalid image file"}), 400


@restaurant_bp.route('/upload_display-image', methods=['POST'])
def upload_display_image():
    image_file = request.files.get('image')
    restaurant_id = request.form.get('restaurantId')

    if not image_file or not restaurant_id:
        return jsonify({"error": "缺少参数"}), 400

    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({"error": "餐厅不存在"}), 404

    # ✅ 正确拼接路径
    filename = secure_filename(image_file.filename)
    upload_dir = os.path.join(current_app.root_path, f'static/restaurant_images/{restaurant_id}/display')
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    image_file.save(filepath)

    # 保存数据库中的相对路径
    new_image = restaurant_images(
        restaurantId=restaurant_id,
        image_path=f"/static/restaurant_images/{restaurant_id}/display/{filename}"
    )
    db.session.add(new_image)
    db.session.commit()

    return jsonify({"message": "图片上传成功", "path": new_image.image_path})



@restaurant_bp.route('/hot-restaurants', methods=['GET'])
def api_get_restaurants():
    try:
        limit = request.args.get('limit', default=None, type=int)

        # 查询餐厅数据
        query = Restaurant.query.order_by(Restaurant.review_count.desc())
        if limit:
            restaurants = query.limit(limit).all()
        else:
            restaurants = query.all()

        result = []
        for r in restaurants:
            result.append({
                "restaurantId": r.restaurantId,
                "name": r.name,
                "address": r.address,
                "cuisine": r.cuisine,
                "description": r.description,
                "createdAt": r.createdAt.isoformat(),
                "image": r.image,
                "review_count": r.review_count,
                "average_rating": r.average_rating
            })

        return jsonify({"restaurants": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
