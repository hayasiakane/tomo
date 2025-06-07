from functools import wraps
from flask import request, redirect, url_for, flash
from app.models.user import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(request.cookies.get('user_id'))
        if not request.cookies.get('user_id'):
            flash('请先登录', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def business_account_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from app.models.user import User
        
        user_id = request.cookies.get('user_id')
        user = User.query.get(user_id)
        if user.type != 'business':
            flash('需要商家账号才能执行此操作', 'danger')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function