from . import db
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash
from gremlin_python.driver import client  # 添加这行
from werkzeug.security import generate_password_hash  # 密码加密需要
from werkzeug.security import check_password_hash   # 密码验证需要
import os
import datetime
from gremlin_python.process.graph_traversal import __ 
class User:
    @staticmethod
    def register(name, email, password, user_type="regular"): # 默认用户类型为普通用户
        """注册新用户"""
        try:
            # 初始化Gremlin客户端（根据你的配置调整）
            #gremlin_client = client.Client('ws://localhost:8182/gremlin', 'g')
            
            # 1. 检查邮箱是否已存在
            auth_data,error = User.get_by_email(email)
            if not error:
                return None,"邮箱已存在"
            
            # 2. 创建新用户（密码加密）
            user_id = str(uuid.uuid4())  # 生成唯一ID
            hashed_pw = generate_password_hash(password)

            # 创建用户顶点
            db.g.addV('user') \
              .property('userId', user_id) \
              .property('name', name) \
              .property('email', email) \
              .property('password', hashed_pw) \
              .property('type', user_type) \
              .property('createdAt', datetime.datetime.now().isoformat()) \
              .next()
            
            return user_id, None
        except Exception as e:
            return None, str(e)
        finally:
            db.close()  # 关闭连接

    @staticmethod
    def authenticate(email, password):
        try:
            # 查询用户数据（参数化查询）
            results = db.g.V()\
                .has('user', 'email', email)\
                .valueMap('userId', 'name', 'email', 'type', 'password')\
                .toList()
                
            if not results:
                return None, "用户不存在"
            
            # Get the first result (should be only one since email should be unique)
            user_data = results[0]
            
            # Check if password exists in the result
            if 'password' not in user_data or not user_data['password']:
                return None, "用户数据不完整"
            
            # 验证密码
            if not check_password_hash(user_data['password'][0], password):
                return None, "密码错误"
            
            return {
                'user_id': user_data['userId'][0] if 'userId' in user_data else None,
                'name': user_data['name'][0] if 'name' in user_data else None,
                'email': user_data['email'][0] if 'email' in user_data else None,
                'type': user_data['type'][0] if 'type' in user_data else None,
            }, None 
    
        except Exception as e:
            return None, f"数据库错误: {str(e)}"
        finally:
            db.close()

    @staticmethod
    def get_by_id(user_id):
        """根据ID获取用户信息"""
        try:
            user = db.g.V().has('user', 'userId', user_id) \
                        .valueMap(True).next()
            
            return {
                'userId': user['userId'][0],
                'name': user['name'][0],
                'email': user['email'][0],
                'type': user['type'][0],
                'createdAt': user['createdAt'][0]
            }, None
        except Exception as e:
            return None, "User not found"
        finally:
            db.close()
    
    @staticmethod
    def get_by_email(user_email):
        """根据ID获取用户信息"""
        try:
            user = db.g.V().has('user', 'email', user_email) \
                        .valueMap(True).next()
            
            return {
                'userId': user['userId'][0],
                'name': user['name'][0],
                'email': user['email'][0],
                'type': user['type'][0],
                'createdAt': user['createdAt'][0]
            }, None
        except Exception as e:
            return None, "User not found"
        finally:
            db.close()
    
    @staticmethod
    def get_by_name(user_name):
        """根据ID获取用户信息"""
        try:
            user = db.g.V().has('user', 'name', user_name) \
                        .valueMap(True).next()
            
            return {
                'userId': user['userId'][0],
                'name': user['name'][0],
                'email': user['email'][0],
                'type': user['type'][0],
                'createdAt': user['createdAt'][0]
            }, None
        except Exception as e:
            return None, "User not found"
        finally:
            db.close()
        
    @staticmethod
    def get(attribute='userId', value=None):
        """根据属性获取用户信息"""
        try:
            user = db.g.V().has('user',attribute, value) \
                        .valueMap(True).next()
            
            return {
                'userId': user['userId'][0],
                'name': user['name'][0],
                'email': user['email'][0],
                'type': user['type'][0],
                'createdAt': user['createdAt'][0]
            }, None
        except Exception as e:
            return None, "User not found"
        finally:
            db.close()

    @staticmethod
    def add_friend(user_id, friend_id):
        """添加好友关系"""
        try:
            # 检查是否已是好友
            existing = db.g.V().has('user', 'userId', user_id) \
                             .out('is_friend') \
                             .has('user', 'userId', friend_id) \
                             .hasNext()
            if existing:
                return False, "Already friends"
            
            # 创建单向好友关系
            db.g.addE('is_friend') \
                   .from_(__.V().has('user', 'userId', user_id)) \
                    .to(__.V().has('user', 'userId', friend_id)) \
                    .next()
            
            return True, None
        except Exception as e:
            return False, str(e)
        finally:
            db.close()

    @staticmethod
    def get_friends(user_id):
        """获取好友列表"""
        try:
            friends = db.g.V().has('user', 'userId', user_id) \
                             .out('is_friend') \
                             .valueMap('name', 'email', 'userId') \
                             .toList()
            return [{
                'userId': f['userId'][0],
                'name': f['name'][0],
                'email': f['email'][0]
            } for f in friends], None
        except Exception as e:
            return None, str(e)
        finally:
            db.close()

    @staticmethod
    def remove_friend(user_id, friend_id):
        """移除好友关系"""
        try:
            # 删除单向关系
            db.g.V().has('user', 'userId', user_id) \
                   .outE('is_friend') \
                   .where(db.g.inV().has('user', 'userId', friend_id)) \
                   .drop() \
                   .iterate()
            
            return True, None
        except Exception as e:
            return False, str(e)
        finally:
            db.close()
        
    @staticmethod
    def delete(attribute='userId', value=None):
        """根据属性删除用户信息"""
        try:
            # 检查顶点是否存在
            if not db.g.V().has('user', attribute, value).hasNext():
                return False  # 顶点不存在，返回 False

            # 删除顶点
            db.g.V().has('user', attribute, value).drop().next()
            return True  # 删除成功
        except Exception as e:
            return  str(e)
        finally:
            db.close()

# @classmethod
# def get_by_id(cls, user_id):
#     try:
#         gremlin_client = client.Client('ws://localhost:8182/gremlin', 'g')
        
#         query = """
#         g.V()
#          .has('user', 'user_id', user_id)
#          .project('user_id', 'name', 'email', 'type', 'created_at', 'last_login')
#          .by(values('user_id'))
#          .by(values('name'))
#          .by(values('email'))
#          .by(values('type'))
#          .by(values('created_at'))
#          .by(coalesce(values('last_login'), constant(null)))
#         """
#         result = gremlin_client.submit(query, {'user_id': user_id}).all().result()
        
#         if not result:
#             return None
            
#         return result[0]
        
#     except Exception as e:
#         raise e
#     finally:
#         gremlin_client.close()
    

