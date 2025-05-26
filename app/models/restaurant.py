from . import db
import uuid
from datetime import datetime
#from gremlin_python.process.traversal import __ 
from gremlin_python.process.graph_traversal import __
log_flag = False  # 是否开启日志记录
if log_flag:
    from flask import current_app 


class Restaurant:
    @staticmethod
    def create(owner_id, name, address, cuisine="", description="",files=None):
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
            restaurant=db.g.addV('restaurant') \
              .property('restaurantId', restaurant_id) \
              .property('name', name) \
              .property('address', address) \
              .property('cuisine', cuisine) \
              .property('description', description) \
              .property('images',[]) \
              .property('createdAt', datetime.now().isoformat()) \
              .next()

            saved_images = []
            if files:
                from utils.file_utils import save_restaurant_images  # 延迟导入避免循环依赖
                saved_image = save_restaurant_images(restaurant_id, files)
                for img in saved_image:
                    saved_images.append(img)
                print(f"Saved images: {saved_images}")
                # 更新顶点属性
                db.g.V(restaurant).property('images', saved_images).next()

            #创建拥有关系
            
            db.g.addE('owns') \
                   .from_( __.V().has('user', 'userId', str(owner_id))) \
                     .to( __.V().has('restaurant', 'restaurantId', restaurant_id)).next() \

            # db.g.V().has('user', 'userId', owner_id) \
            #        .addE('owns') \
            #        .to( __.V().has('restaurant', 'restaurantId', restaurant_id)) \
            #        .next()
            
            return restaurant_id, None
        except Exception as e:
            return None, str(e)
        finally:
            db.close()  # 关闭连接

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
                'images': restaurant.get('images', []),
                'createdAt': restaurant['createdAt'][0],
                'owner': {
                    'userId': owner['userId'][0],
                    'name': owner['name'][0]
                },
                'reviewCount': review_count
            }, None
        except Exception as e:
            return None, "Restaurant not found"
        finally:
            db.close()  # 关闭连接

    @staticmethod  
    def get(attribut='restaurantId', value=None):
        """根据属性获取餐厅信息"""
        try:
            restaurant = db.g.V().has('restaurant', attribut, value) \
                               .valueMap(True).next()
            
            # 获取所有者信息
            owner = db.g.V().has('restaurant', attribut, value) \
                          .in_('owns') \
                          .valueMap('name', 'userId').next()
            
            # # 获取评价数量
            # review_count = db.g.V().has('restaurant', attribut, value) \
            #                      .in_('has_review') \
            #                      .count().next()
            # 返回餐厅信息   
            return {
                'restaurantId': restaurant['restaurantId'][0],
                'name': restaurant['name'][0],
                'address': restaurant['address'][0],
                'cuisine': restaurant.get('cuisine', [''])[0],
                'description': restaurant.get('description', [''])[0],
                'images': restaurant.get('images', []),
                'createdAt': restaurant['createdAt'][0],
                'owner': {
                    'userId': owner['userId'][0],
                    'name': owner['name'][0]
                },
                #'reviewCount': review_count
            }, None
        except Exception as e:
            return None, str(e)
        finally:
            db.close()  # 关闭连接
        

    @staticmethod   
    def get_all( search=None, cuisine=None): #page=1, per_page=10,
        """获取餐厅列表"""
        try:
            # 构建基础查询（用于分页数据）
            data_traversal = db.g.V().hasLabel('restaurant')
            
            # 应用搜索条件
            if search:
                data_traversal = data_traversal.has('name', search)
            
            # 应用菜系过滤
            if cuisine:
                data_traversal = data_traversal.has('cuisine', cuisine)
            
            # 执行分页查询
            restaurants = data_traversal \
                                    .valueMap('name', 'address', 'cuisine', 'restaurantId','image') \
                                    .toList()
            #.range((page-1)*per_page, page*per_page)
            # 重新构建查询计算总数（不能复用 data_traversal）
            count_traversal = db.g.V().hasLabel('restaurant')
            if search:
                count_traversal = count_traversal.has('name', search)
            if cuisine:
                count_traversal = count_traversal.has('cuisine', cuisine)
            
            total = count_traversal.count().next()
            
            return {
                'restaurants': [{
                    'restaurantId': r['restaurantId'][0],
                    'name': r['name'][0],
                    'address': r['address'][0],
                    'cuisine': r.get('cuisine', [''])[0],
                    'images': r.get('images', [])
                } for r in restaurants],
                'total': total,
                # 'page': page,
                # 'per_page': per_page
            }, None
        except Exception as e:
            return None, str(e)
        finally:
            db.close()

    @staticmethod
    def delete(attribute='restaurantId',value=None):
        """删除餐厅"""
        try:
            # 删除相关评价和回复
            db.g.V().has('restaurant', attribute, value) \
                   .in_('has_review') \
                   .in_('has_reply') \
                   .drop() \
                   .iterate()
            
            db.g.V().has('restaurant', attribute,value) \
                   .in_('has_review') \
                   .drop() \
                   .iterate()
            
            # 删除餐厅顶点
            db.g.V().has('restaurant', attribute,value) \
                   .drop() \
                   .iterate()
            
            return True, None
        except Exception as e:
            return False, str(e)
        finally:
            db.close()

    @staticmethod
    def get_by_owner(attribute='userId',value=None):
        """获取用户拥有的餐厅"""
        try:
            restaurants = db.g.V().has('user', attribute, value) \
                                .out('owns') \
                                .valueMap('name', 'address', 'cuisine', 'restaurantId') \
                                .toList()
            
            return [{
                'restaurantId': r['restaurantId'][0],
                'name': r['name'][0],
                'address': r['address'][0],
                'images': r.get('images', []),
                'cuisine': r.get('cuisine', [''])[0]
            } for r in restaurants], None
        except Exception as e:
            return None, str(e)
        finally:
            db.close()

    @staticmethod
    def add_images(restaurant_id, images):
        """增加餐厅图片"""
        try:
            save_images=[]
            if images:
                from utils.file_utils import save_restaurant_images  # 延迟导入避免循环依赖
                # 保存图片 
                save_images=save_restaurant_images(restaurant_id, images)
            print("fuck1")
            res=db.g.V().has('restaurant', 'restaurantId',restaurant_id).valueMap(True).next()  # 获取当前餐厅的图片列表
            imgs=res.get('images', [])  # 获取当前餐厅的图片列表
            for img in save_images:
                imgs.append(img)  # 添加新图片到列表
            print("add res image: ",restaurant_id,imgs)
            # 更新顶点属性
            db.g.V().has('restaurant', 'restaurantId',restaurant_id) \
                   .property('images', imgs) \
                   .next()
            print("fuck")
            if log_flag:
                current_app.logger.info(f"add res image: {restaurant_id} at {save_images[0]}")
            return True, None
        except Exception as e:
            if log_flag:
                current_app.logger.error(f"Failed to add user image: {restaurant_id} - {str(e)}")
            return False, str(e)
        finally:
            db.close()
    
    @staticmethod
    def delete_all_images(restaurant_id):
        """删除全部餐厅图片"""
        try:
            
            from utils.file_utils import delete_restaurant_images  # 延迟导入避免循环依赖
            # 保存图片 
            save_images=delete_restaurant_images(restaurant_id)

            # 更新顶点属性
            db.g.V().has('restaurant', 'restaurantId',restaurant_id) \
                   .property('images', []) \
                   .next()
            if log_flag:
                current_app.logger.info(f"deleted all  res image: {restaurant_id} ")
            return True, None
        except Exception as e:
            if log_flag:
                current_app.logger.error(f"Failed to delete user image: {restaurant_id} - {str(e)}")
            return False, str(e)
        finally:
            db.close()

    @staticmethod
    def delete_image(restaurant_id,filename=""):
        """增加单张餐厅图片"""
        try:
            if not filename=="":
                from utils.file_utils import delete_restaurant_images  # 延迟导入避免循环依赖
                # 保存图片 
                save_images=delete_restaurant_images(restaurant_id,filename)

            restaurant=db.g.V().has('restaurant', 'restaurantId',restaurant_id).value('images').next()  # 获取当前餐厅的图片列表
            new_images = [img for img in restaurant if img != filename]  # 删除指定图片
            # 更新顶点属性
            db.g.V().has('restaurant', 'restaurantId',restaurant_id) \
                   .property('images', new_images) \
                   .next()
            if log_flag:
                current_app.logger.info(f"deleted specific  res image: {restaurant_id} ")
            return True, None
        except Exception as e:
            if log_flag:
                current_app.logger.error(f"Failed to delete specific res image: {restaurant_id} - {str(e)}")
            return False, str(e)
        finally:
            db.close()