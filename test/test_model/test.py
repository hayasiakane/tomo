import sys
import os

# 获取 app 目录的父目录
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 将父目录添加到 sys.path
sys.path.append(parent_dir)
print(f"Parent directory: {parent_dir}")
from app.models import db
from app.models.user import User

def test_db_connection():
    try:
        db.g.addV('test').property('name', 'test').next()  # 测试添加一个顶点
        print("连接成功！顶点数量:", db.g.V().count().next())
        db.close()  # 关闭连接
    except Exception as e:
        print("连接失败:", str(e))

def test_reg():
    # 测试注册用户
    data = {
        'name': 'test_user3',
        'email': '124@124.com',
        'password':'123456',
        'type': 'regular',
        }
    id,error=User.register(data['name'], data['email'], data['password'], data.get('type', 'regular'))
    return id,error

def search_user_by_email(email):
    # 测试根据邮箱搜索用户
    user, error = User.get_by_email(email)
    if error:
        print("Error:", error)
    else:
        print("User found:", user['userId'])
id,error=test_reg()
if not error:
    print("创建的用户的id是:",id)
else:
    print("创建用户失败:", error)
search_user_by_email('123@123.com')
test_db_connection()