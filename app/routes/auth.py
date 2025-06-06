import sys
import os
from app.extensions import db  # 导入数据库
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_jwt_extended import create_access_token  # 导入JWT相关函数
# from werkzeug.security import check_password_hash  # 导入密码哈希验证函数
from app.models.user import User  # 导入User模型
from datetime import datetime  # 直接导入datetime类
import uuid # 导入UUID生成器,用于生成唯一的用户ID

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

    # print("Received data:", data)  # 打印日志
    # 认证用户
    user = User.query.filter_by(email=data['email']).first()
    # print("User found:", user)  # 打印日志
    if not user or user.password != data['password']:  # 注意：实际项目中应使用哈希密码验证
        return jsonify({"error": "无效的邮箱或密码"}), 401
    
    token = create_access_token(identity=str(user.userId)) # 生成JWT令牌，identity为用户ID

    # 生成响应（实际项目应使用JWT）
    return jsonify({
        "message": "登录成功",
        "userId": user.userId,
        "name": user.name,
        "token": token,
        "type": user.type
    }), 200

@auth_bp.route('/register', methods=['GET'])
def show_register_page():
    return render_template('auth/register.html')

@auth_bp.route('/api/users/register', methods=['POST'])
def api_register():
    # 检查请求是否为JSON格式
    if not request.is_json:
        return jsonify({"error": "Unsupported Media Type: Content-Type must be application/json"}), 415

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # 简单的输入验证
    if not name or not email or not password:
        return jsonify({"message": "Name, email, and password are required"}), 400

    # 检查邮箱是否已被注册
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already registered"}), 400

    # 创建新用户对象
    new_user = User(
        userId=str(uuid.uuid4()),  # 使用UUID生成唯一的用户ID
        name=name,
        email=email,
        password=password,  # 注意：实际项目中应使用哈希密码
        type='regular',  # 默认用户类型
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while registering user", "error": str(e)}), 500



@auth_bp.route('/logout')
def logout():
    response = redirect(url_for('main.index'))
    response.delete_cookie('user_id')
    flash('您已成功退出', 'success')
    return response

@auth_bp.route('/profile', methods=['GET'])
def get_user_profile(user_id):
    # 从数据库中获取用户信息
    user = User.query.get(user_id)
    if not user:
        flash('用户不存在', 'danger')
        return redirect(url_for('base.index'))
    
    # 渲染用户个人资料页面
    return render_template('user/profile.html', user=user)