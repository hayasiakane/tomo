from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.user import User
from app.utils.decorators import login_required
from werkzeug.security import generate_password_hash
from gremlin_python.driver import client
import uuid
import datetime
user_bp = Blueprint('user', __name__, url_prefix='')  # 不加 /user 前缀

@user_bp.route('/profile/<userid>')
@login_required
def profile():
    user_id = request.cookies.get('user_id')
    user, error = User.get_by_id(user_id)
    if error:
        flash(error, 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('user/profile.html', user=user)


@user_bp.route('/friends')
def friends():
    return render_template('user/friends.html')

# 新增通过用户ID获取用户信息的API
@user_bp.route('/api/users/<userId>', methods=['GET'])
def api_get_user(userId):
    user, error = User.get_by_id(userId)
    if error:
        return {'error': error}, 404
    
    # 返回用户信息（过滤敏感字段）
    response_data = {
        'userId': user['userId'],
        'name': user['name'],
        'email': user['email'],
        'type': user['type'],
        'createdAt': user['createdAt']
    }

    return jsonify(response_data), 200

@user_bp.route('/edit_profile.html')
def edit_profile():
    return render_template('user/edit_profile.html')


# 用于更新用户昵称
@user_bp.route('/api/users/update', methods=['PUT'])
def update_user_profile():
    data = request.get_json()
    user_id = data.get("userId")
    new_name = data.get("name")

    if not user_id or not new_name:
        return jsonify({"error": "缺少参数"}), 400

    success, error = User.update_name(user_id, new_name)
    if not success:
        return jsonify({"error": error}), 500

    return jsonify({"message": "用户昵称已更新"}), 200
