import sys
import os

# 获取 app 目录的父目录
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))))
# 将父目录添加到 sys.path
sys.path.append(parent_dir)
#print(f"Parent directory: {parent_dir}")
from app.models import db
from app.models.user import User
from app.models.friendship import Friendship

create=1

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

if create:
    id=test_reg()

User.add_friend(id[0],id[1])  #0,1 有共同好友2
User.add_friend(id[0],id[2])  #给0推荐好友3.
User.add_friend(id[2],id[3])
User.add_friend(id[1],id[2])

comfri_data,error=Friendship.get_common_friends(id[0],id[1])
if error:
    print("Error:", error)
else:
    print("共同好友:", comfri_data)
#推荐好友测试

# recommendations, error = Friendship.get_friend_recommendations('userId', id[0])
# if error:
#     print("Error:", error)
# else: 
#     print("好友推荐:", recommendations)
#推荐好友测试