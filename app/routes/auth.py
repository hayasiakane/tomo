import sys
import os

# 获取 app 目录的父目录
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 将父目录添加到 sys.path
sys.path.append(parent_dir)
print(f"Parent directory: {parent_dir}")

from flask import Blueprint, render_template, request, redirect, url_for, flash
from gremlin_python.driver import client  # 添加这行
from werkzeug.security import generate_password_hash,check_password_hash  # 密码加密需要
from app.models.user import User
from flask import Blueprint, request, jsonify
from datetime import datetime  # 直接导入datetime类
import uuid
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET'])
def login():
    
    
    return render_template('auth/login.html')

@auth_bp.route('/api/users/login', methods=['POST'])
def api_login():
    # 强制JSON解析
    try:
        data = request.get_json(force=True)
    except:
        return jsonify({"error": "需要JSON格式数据"}), 400
    
    # 验证必填字段
    if not all(k in data for k in ['email', 'password']):
        return jsonify({"error": "缺少邮箱或密码"}), 400
    
    # 认证用户
    user, error = User.authenticate(data['email'], data['password'])
    if error:
        return jsonify({"error": error}), 401
    
    # 生成响应（实际项目应使用JWT）
    return jsonify({
        "message": "登录成功",
        "userId": user['user_id'],
        "name": user['name'],
        "token": "模拟Token",  # 生产环境替换为真实JWT
        "type": user['type']
    }), 200

@auth_bp.route('/register', methods=['GET'])
def show_register_page():
    return render_template('auth/register.html')

@auth_bp.route('/api/users/register', methods=['POST'])
def api_register():
    # 验证Content-Type
    if not request.is_json:
        return jsonify({"error": "Unsupported Media Type: Content-Type must be application/json"}), 415
    
    data = request.get_json()

    # 必填字段验证
    required_fields = ['name', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        # 初始化Gremlin连接
        gremlin_client = client.Client('ws://localhost:8182/gremlin', 'g')
        
        
        # #hashed_pw = generate_password_hash(data['password'])
        # #user_id = str(uuid.uuid4())  # 生成唯一ID
        # if result[0] > 0:
        #     return jsonify({"error": "Email already exists"}), 400
        
        User.register(data['name'], data['email'], data['password'], data.get('type', 'regular'))
        # 执行创建用户的Gremlin查询
        user_data,error = User.get_by_email(data['email'])
        if error:
            return jsonify({"error": "User creation failed"}), 500
        return jsonify({
            "message": "Registration successful",
            "userId": user_data['userId'],
            "username": user_data['name'],
            "type": user_data['type'],
            "token": "模拟Token",  # 生产环境替换为真实JWT
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'gremlin_client' in locals():
            gremlin_client.close()

@auth_bp.route('/logout')
def logout():
    response = redirect(url_for('main.index'))
    response.delete_cookie('user_id')
    flash('您已成功退出', 'success')
    return response

@auth_bp.route('/profile', methods=['GET'])
def get_user_profile(user_id):
    try:
        # 从数据库获取用户信息
        user_data = User.get_by_id(user_id)
        if not user_data:
            return jsonify({"error": "用户不存在"}), 404
            
        return jsonify({
            "user_id": user_data["user_id"],
            "name": user_data["name"],
            "email": user_data["email"],
            "type": user_data["type"],
            "created_at": user_data["created_at"],
            "last_login": user_data.get("last_login")
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500