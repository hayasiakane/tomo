from . import db
import uuid
from datetime import datetime

class Restaurant:
    @staticmethod
    def create(owner_id, name, address, cuisine="", description=""):
        """创建新餐厅"""
        try:
            # 检查餐厅是否已存在
            existing = db.g.V().has('restaurant', 'name', name) \
                             .has('address', address) \
                             .hasNext()
            if existing:
                return None, "Restaurant already exists"
            
            # 创建餐厅顶点
            restaurant_id = str(uuid.uuid4())
            db.g.addV('restaurant') \
              .property('restaurantId', restaurant_id) \
              .property('name', name) \
              .property('address', address) \
              .property('cuisine', cuisine) \
              .property('description', description) \
              .property('createdAt', datetime.now().isoformat()) \
              .next()
            
            # 创建拥有关系
            db.g.V().has('user', 'userId', owner_id) \
                   .addE('owns') \
                   .to(__.V().has('restaurant', 'restaurantId', restaurant_id)) \
                   .next()
            
            return restaurant_id, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_by_id(restaurant_id):
        """根据ID获取餐厅信息"""
        try:
            restaurant = db.g.V().has('restaurant', 'restaurantId', restaurant_id) \
                               .valueMap(True).next()
            
            # 获取所有者信息
            owner = db.g.V().has('restaurant', 'restaurantId', restaurant_id) \
                          .in_('owns') \
                          .valueMap('name', 'userId').next()
            
            # 获取评价数量
            review_count = db.g.V().has('restaurant', 'restaurantId', restaurant_id) \
                                 .in_('has_review') \
                                 .count().next()
            
            return {
                'restaurantId': restaurant['restaurantId'][0],
                'name': restaurant['name'][0],
                'address': restaurant['address'][0],
                'cuisine': restaurant.get('cuisine', [''])[0],
                'description': restaurant.get('description', [''])[0],
                'createdAt': restaurant['createdAt'][0],
                'owner': {
                    'userId': owner['userId'][0],
                    'name': owner['name'][0]
                },
                'reviewCount': review_count
            }, None
        except Exception as e:
            return None, "Restaurant not found"

    @staticmethod
    def get_all(page=1, per_page=10, search=None, cuisine=None):
        """获取餐厅列表"""
        try:
            # 基本查询
            traversal = db.g.V().hasLabel('restaurant')
            
            # 应用搜索条件
            if search:
                traversal = traversal.has('name', search)
            
            # 应用菜系过滤
            if cuisine:
                traversal = traversal.has('cuisine', cuisine)
            
            # 分页
            restaurants = traversal.range((page-1)*per_page, page*per_page) \
                                 .valueMap('name', 'address', 'cuisine', 'restaurantId') \
                                 .toList()
            
            # 获取总数
            total = traversal.count().next()
            
            return {
                'restaurants': [{
                    'restaurantId': r['restaurantId'][0],
                    'name': r['name'][0],
                    'address': r['address'][0],
                    'cuisine': r.get('cuisine', [''])[0]
                } for r in restaurants],
                'total': total,
                'page': page,
                'per_page': per_page
            }, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def delete(restaurant_id):
        """删除餐厅"""
        try:
            # 删除相关评价和回复
            db.g.V().has('restaurant', 'restaurantId', restaurant_id) \
                   .in_('has_review') \
                   .in_('has_reply') \
                   .drop() \
                   .iterate()
            
            db.g.V().has('restaurant', 'restaurantId', restaurant_id) \
                   .in_('has_review') \
                   .drop() \
                   .iterate()
            
            # 删除餐厅顶点
            db.g.V().has('restaurant', 'restaurantId', restaurant_id) \
                   .drop() \
                   .iterate()
            
            return True, None
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_by_owner(owner_id):
        """获取用户拥有的餐厅"""
        try:
            restaurants = db.g.V().has('user', 'userId', owner_id) \
                                .out('owns') \
                                .valueMap('name', 'address', 'cuisine', 'restaurantId') \
                                .toList()
            
            return [{
                'restaurantId': r['restaurantId'][0],
                'name': r['name'][0],
                'address': r['address'][0],
                'cuisine': r.get('cuisine', [''])[0]
            } for r in restaurants], None
        except Exception as e:
            return None, str(e)