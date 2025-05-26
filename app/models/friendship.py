from . import db
from gremlin_python.process.graph_traversal import __ 
from gremlin_python.process.traversal import T, P
class Friendship:
    @staticmethod
    def get_friend_recommendations(attribute='userId', value=None,limit=5):
        """获取好友推荐（基于好友的好友）"""
        try:
                # 获取当前用户顶点
            current_user = db.g.V().has('user', attribute, value).next()
            # 获取直接好友列表（用于后续过滤）
            friends = db.g.V().has('user', attribute, value).both('is_friend').id_().toList()
            # 获取二度人脉（排除自己和直接好友）
            recommendations = (
            db.g.V().has('user', attribute, value)
            .both('is_friend')  # 一度人脉
            .both('is_friend')  # 二度人脉
            .has(T.id, P.neq(current_user.id))  # ✅ 排除自己（使用 T.id 和 P.neq）
            .has(T.id, P.without(*friends))     # ✅ 排除直接好友（使用 P.without）
            .dedup()
            .limit(limit)
            .valueMap('name', 'email', 'userId')
            .toList()
        )
            
            return [{
                'userId': r['userId'][0],
                'name': r['name'][0],
                'email': r['email'][0]
            } for r in recommendations], None
        except Exception as e:
            return None, str(e)
        finally:
            db.close()

    @staticmethod
    def get_common_friends(user_id, friend_id):
        """获取共同好友"""
        try:
            common_friends = db.g.V().has('user', 'userId', user_id) \
                                   .both('is_friend') \
                                   .where(__.in_('is_friend') \
                                          .has('user', 'userId', friend_id)) \
                                   .valueMap('name', 'email', 'userId') \
                                   .toList()
            
            return [{
                'userId': f['userId'][0],
                'name': f['name'][0],
                'email': f['email'][0]
            } for f in common_friends], None
        except Exception as e:
            return None, str(e)
        finally:
            db.close()