from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.user import User
from app.utils.decorators import login_required
from werkzeug.security import generate_password_hash
from gremlin_python.driver import client
import uuid
import datetime
user_bp = Blueprint('user', __name__)

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
@login_required
def friends():
    user_id = request.cookies.get('user_id')
    friends, error = User.get_friends(user_id)
    if error:
        flash(error, 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('user/friends.html', friends=friends) #friends.html未生成

class User:
    @classmethod
    def register(cls, name, email, password, user_type):
        try:
            # 初始化Gremlin客户端（根据你的配置调整）
            gremlin_client = client.Client('ws://localhost:8182/gremlin', 'g')
            
            # 1. 检查邮箱是否已存在（使用参数化查询防止注入）
            email_check = "g.V().has('user', 'email', email).count()"
            result = gremlin_client.submit(email_check, {'email': email}).all().result()
            
            if result[0] > 0:
                return None, "该邮箱已被注册"
            
            # 2. 创建新用户（密码加密）
            user_id = str(uuid.uuid4())  # 生成唯一ID
            hashed_pw = generate_password_hash(password)
            
            create_query = """
            g.addV('user')
             .property('id', id)
             .property('name', name)
             .property('email', email)
             .property('password', password)
             .property('type', type)
             .property('created_at', created_at)
            """
            
            gremlin_client.submit(create_query, {
                'id': user_id,
                'name': name,
                'email': email,
                'password': hashed_pw,
                'type': user_type,
                'created_at': datetime.datetime.now().isoformat()
            }).all().result()
            
            return user_id, None
            
        except Exception as e:
            return None, str(e)
        finally:
            gremlin_client.close()  # 关闭连接