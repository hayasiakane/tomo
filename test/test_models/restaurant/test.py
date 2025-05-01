import sys
import os

# 获取 app 目录的父目录
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))))
# 将父目录添加到 sys.path
sys.path.append(parent_dir)

from app.models import db
from app.models.user import User
from app.models.restaurant import Restaurant
from gremlin_python.process.graph_traversal import __
#测试注册用户

create=0

test_user_name=['test_user','test_user1','test_user2','test_user3']
test_user_email=['123@123.com','124@124.com','125@125.com','126@126.com']
test_user_password=['123456','123456','123456','123456']
test_user_type=['business','business','business','business']
def test_reg():
    # 测试注册用户
    user_ids = []
    for i in range(4):
        data = {
            'name': test_user_name[i],
            'email': test_user_email[i],
            'password':test_user_password[i],
            'type': test_user_type[i],
        }
        id,error=User.register(data['name'], data['email'], data['password'], data.get('type', 'regular'))
        if error:
            print("Error:", error)
        else:
            print("User created with ID:", id)
            user_ids.append(id)
    return user_ids

#邮箱查询用户测试
def search_user_by_email(email):
    # 测试根据邮箱搜索用户
    user, error = User.get_by_email(email)
    if error:
        print("Error:", error)
    else:
        print("User found:", user['userId'])

if create:
    id=test_reg()
    id,error=User.get('name','test_user')
    if not error:
        print("创建的用户的id是:",id)
    else:
        print("创建用户失败:", error)

test_name=['test_restaurant','test_restaurant1','test_restaurant2','test_restaurant3']
test_address=['123 Test St','456 Test Ave','789 Test Blvd','101 Test Rd']
test_cusine=['Italian','Chinese','Mexican','Indian']
test_description=['A test restaurant','A test restaurant1','A test restaurant2','A test restaurant3']

#餐厅创建测试函数
def test_create_restaurant():
    
    for i in range(4):
        data = {
            'name': test_name[i],
            'address': test_address[i],
            'cuisine': test_cusine[i],
            'description': test_description[i]
        }
        user_id = id[i]  # 替换为实际的用户ID
        restaurant_id, error = Restaurant.create(
            owner_id=user_id,
            name=data['name'],
            address=data['address'],
            cuisine=data['cuisine'],
            description=data['description']
        )
        if error:
            print("Error:", error)
        else:
            print("Restaurant created with ID:", restaurant_id)

#建立边失败的话，即使建立了餐厅的点，最后也不会返回餐厅的id
if create:
    test_create_restaurant()
# 测试根据餐厅名称获取餐厅信息,且测试删除功能
data,error=Restaurant.get_all()
if error:
    print("Error:", error)
else:
    print("Restaurant found:", data)
#     # 删除餐厅
#     restaurant_id = data['restaurantId']
#     error = Restaurant.delete(restaurant_id)
#     if error:
#         print("Error:", error)
#     else:
#         print("Restaurant deleted successfully")

# data,error=Restaurant.get('name','test_restaurant')

# if error:
#     print("Error:", error)