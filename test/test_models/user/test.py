import sys
import os
from werkzeug.datastructures import FileStorage
# 获取 app 目录的父目录
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))))
# 将父目录添加到 sys.path
sys.path.append(parent_dir)
#print(f"Parent directory: {parent_dir}")
from app.models import db
from app.models.user import User
from app.models.restaurant import Restaurant


test_images =  [FileStorage(
                stream=open('./app/static/images/friends-dining.jpg', 'rb'),
                filename='test1.jpg')]
            
files = {'images': test_images}

login_flag=False

#数据库连接测试
def test_db_connection():
    try:
        db.g.addV('test').property('name', 'test').next()  # 测试添加一个顶点
        print("连接成功！顶点数量:", db.g.V().count().next())
        db.close()  # 关闭连接
    except Exception as e:
        print("连接失败:", str(e))

#测试注册用户
def test_reg():
    # 测试注册用户
    data = {
        'name': 'test',
        'email': '118@128.com',
        'password':'123456',
        'image': [],
        'type': 'business',
        }
    id,error=User.register(data['name'], data['email'], data['password'], data.get('type', 'regular'),files)
    return id,data['email'],error

#邮箱查询用户测试
def search_user_by_email(email):
    # 测试根据邮箱搜索用户
    user, error = User.get_by_email(email)
    if error:
        print("Error:", error)
    else:
        print("User found:", user['userId'])
if login_flag:
    id,email,error=test_reg()
    if not error:
        print("创建的用户的id是:",id)
    else:
        print("创建用户失败:", error)

#print(search_user_by_email('123@123.com'))
#print(User.delete('email','123@123.com'))
#test_db_connection()

#de,er=User.update_image('61fcb748-3814-4517-8d55-e0c3830a8e66',files)

data,er=User.get_by_id('61fcb748-3814-4517-8d55-e0c3830a8e66')
print("查询用户数据:", data)

if login_flag:
    res,error=User.authenticate(email,'123456')
    if res:
        print("用户登录成功:", res)
    else:
        print("用户登录失败:", error)