from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.user import User
from app.models.friendship import friendships
from app.models.restaurant import Restaurant
from app.models.review import review
from app.utils.decorators import login_required
from werkzeug.security import generate_password_hash
import uuid
import datetime
from app.extensions import db
import os
from werkzeug.utils import secure_filename
from flask import current_app

user_bp = Blueprint('user', __name__, url_prefix='')  # 不加 /user 前缀

@user_bp.route('/profile/<userid>')
# @login_required
def profile(userid):
    user = User.query.get(userid)
    if not user:
        flash("用户不存在", "error")
    
    return render_template('user/profile.html', user=user)


@user_bp.route('/friends')
def friends():
    return render_template('user/friends.html')

# 新增通过用户ID获取用户信息的API
@user_bp.route('/api/users/<userId>', methods=['GET'])
def api_get_user(userId):
    user = User.query.get(userId)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    # 返回用户信息（过滤敏感字段）
    response_data = {
        'userId': user.userId,
        'name': user.name,
        'image': user.image,
        'email': user.email,
        'type': user.type,
        'createdAt': user.createdAt.strftime('%Y-%m-%d %H:%M:%S')
    }

    return jsonify(response_data), 200

@user_bp.route('/edit_profile')
def edit_profile():
    return render_template('user/edit_profile.html')


# 修改用户资料的API
@user_bp.route('/api/users/update', methods=['POST'])
def update_user_profile():
    user_id = request.form.get("userId")
    new_name = request.form.get("name")
    image_file = request.files.get("image")

    if not user_id:
        return jsonify({"error": "缺少用户ID"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    # ✅ 更新昵称（如果提供）
    if new_name:
        user.name = new_name

    # ✅ 上传头像（如果提供）
    if image_file:
        # 先将原头像文件删除（如果存在）
        if user.image:
            try:
                old_image_path = os.path.join(current_app.root_path, user.image.lstrip('/'))
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            except Exception as e:
                print(f"删除旧头像失败: {e}")
        filename = secure_filename(image_file.filename)
        upload_dir = os.path.join(current_app.root_path, f'static/user_avatar/{user_id}')
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, filename)
        image_file.save(filepath)

        # 保存数据库路径（前端可直接访问的相对路径）
        user.image = f"/static/user_avatar/{user_id}/{filename}"

    db.session.commit()

    return jsonify({"message": "用户资料已更新"}), 200




@user_bp.route('/api/friends/list/<int:user_id>', methods=['GET'])
def get_friend_list(user_id):
    """ 获取用户的好友列表 """
    friends = friendships.query.filter_by(userId=user_id).all()
    if not friends:
        return jsonify({"message": "没有好友"}), 404

    friend_list = []
    for friend in friends:
        friend_info = api_get_user(friend.friend_id)
        if friend_info[1] == 200:
            friend_list.append(friend_info[0].get_json())

    return jsonify(friend_list), 200


@user_bp.route('/user/<int:userid>/friend_profile/<int:friendid>', methods=['GET'])
# @login_required
def friend_profile(userid, friendid):
    """ 查看好友的个人资料 """
    friend_info = User.query.get(friendid)# get函数通过主键获取信息
    # 获取用户信息
    restaurants = Restaurant.query.filter_by(userId=friendid).all()
    reviews = review.query.filter_by(userId=friendid).all()
    # 在每条review中添加restaurant_name字段
    for r in reviews:
        restaurant = Restaurant.query.get(r.restaurantId)
        if restaurant:
            r.restaurant_name = restaurant.name
        else:
            r.restaurant_name = "未知餐厅"

    existing_friendship = friendships.query.filter_by(userId=userid, friend_id=friendid).first()
        
    return render_template('user/friend_profile.html',
                            friend=friend_info, 
                            restaurant=restaurants, 
                            reviews=reviews,
                            current_user_id=userid,
                            is_following=existing_friendship is not None)


@user_bp.route('/api/users/<int:user_id>/follow/<int:friend_id>', methods=['POST'])
def follow_user(user_id, friend_id):
    if user_id == friend_id:
        return jsonify({"error": "不能关注自己"}), 400

    existing = friendships.query.filter_by(userId=user_id, friend_id=friend_id).first()
    if existing:
        return jsonify({"message": "已关注"}), 200

    new_relation = friendships(userId=user_id, friend_id=friend_id)
    db.session.add(new_relation)
    db.session.commit()
    return jsonify({"message": "关注成功"}), 201

@user_bp.route('/api/users/<int:user_id>/follow/<int:friend_id>', methods=['DELETE'])
def unfollow_user(user_id, friend_id):
    relation = friendships.query.filter_by(userId=user_id, friend_id=friend_id).first()
    if not relation:
        return jsonify({"message": "尚未关注"}), 200

    db.session.delete(relation)
    db.session.commit()
    return jsonify({"message": "已取消关注"}), 200
