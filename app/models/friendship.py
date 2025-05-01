from . import db
from gremlin_python.process.traversal import __ 
class Friendship:
    @staticmethod
    def get_friend_recommendations(user_id, limit=5):
        """获取好友推荐（基于好友的好友）"""
        try:
            # 获取好友的好友（排除已经是好友的和自己）
            recommendations = db.g.V().has('user', 'userId', user_id) \
                                   .both('is_friend') \
                                   .both('is_friend') \
                                   .where(__.neq(__.V().has('user', 'userId', user_id))) \
                                   .where(__.not_(__.in_('is_friend') \
                                           .has('user', 'userId', user_id))) \
                                   .dedup() \
                                   .limit(limit) \
                                   .valueMap('name', 'email', 'userId') \
                                   .toList()
            
            return [{
                'userId': r['userId'][0],
                'name': r['name'][0],
                'email': r['email'][0]
            } for r in recommendations], None
        except Exception as e:
            return None, str(e)

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