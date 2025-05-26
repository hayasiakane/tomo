from app.models import db
import uuid
from datetime import datetime
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import Order
class Review:
    @staticmethod
    def create(user_id, restaurant_id, content, rating,files=None):
        """创建评价"""
        try:
            # 验证评分范围
            if not 1 <= rating <= 5:
                return None, "Rating must be between 1 and 5"
            
             # 检查用户唯一性
            user = db.g.V().has('user', 'userId', user_id).next()  # 唯一用户顶点
            # 检查餐厅唯一性
            restaurant = db.g.V().has('restaurant', 'restaurantId', restaurant_id).next()  # 唯一餐厅顶点
            
            # 创建评价顶点
            review_id = str(uuid.uuid4())
            review = db.g.addV('review') \
            .property('reviewId', review_id) \
            .property('content', content) \
            .property('rating', rating) \
            .property('pin', False) \
            .property('like', 0) \
            .property('images', [])\
            .property('createdAt', datetime.now().isoformat()) \
            .next()

            saved_images = []
            if files:
                from utils.file_utils import save_review_images  # 延迟导入避免循环依赖
                saved_images = save_review_images(review_id, files)
                # 更新顶点属性
                db.g.V(review).property('images', saved_images).next()
            
            # 创建用户->评价边（精确写法）
            db.g.addE('wrote').from_(user).to(review).next()
            db.close()
            # 创建餐厅<-评价边（精确写法）
            db.g.addE('has_review').from_(restaurant).to(review).next()
                
            return review_id, None
        except Exception as e:
            return None, str(e)
        finally:
            db.close()

    @staticmethod
    def get_by_restaurant(restaurant_id, sort='latest'):
        """获取餐厅的评价"""
        try:
            # 基本查询
            traversal = db.g.V().has('restaurant', 'restaurantId', restaurant_id) \
                              .out('has_review')
            
            # 应用排序
            if sort == 'highest':
                traversal = traversal.order().by('rating',Order.desc)
            elif sort == 'lowest':
                traversal = traversal.order().by('rating')
            else:  # latest
                traversal = traversal.order().by('createdAt',Order.desc)
            
            reviews = traversal.project('review', 'user', 'reply') \
                              .by(__.valueMap(True)) \
                              .by(__.in_('wrote').valueMap('name', 'userId')) \
                              .by(__.out('has_reply').valueMap(True).fold()) \
                              .toList()
            
            return [{
                'reviewId': r['review']['reviewId'][0],
                'content': r['review']['content'][0],
                'rating': r['review']['rating'][0],
                'pin': r['review']['pin'][0],
                'like': r['review']['like'][0],
                'images': r['review'].get('images', []),
                'createdAt': r['review']['createdAt'][0],
                'user': {
                    'userId': r['user']['userId'][0],
                    'name': r['user']['name'][0]
                },
                'reply': {
                    'content': r['reply'][0]['content'][0],
                    'createdAt': r['reply'][0]['createdAt'][0]
                } if r['reply'] else None
            } for r in reviews], None
        except Exception as e:
            return None, str(e)
        finally:
            db.close()

    @staticmethod
    def get_by_user(user_id):
        """获取用户的评价"""
        try:
            reviews = db.g.V().has('user', 'userId', user_id) \
                            .out('wrote') \
                            .project('review', 'restaurant') \
                            .by(__.valueMap(True)) \
                            .by(__.in_('has_review').valueMap('name', 'restaurantId')) \
                            .toList()
            
            return [{
                'reviewId': r['review']['reviewId'][0],
                'content': r['review']['content'][0],
                'rating': r['review']['rating'][0],
                'images': r['review'].get('images', []),
                'createdAt': r['review']['createdAt'][0],
                'restaurant': {
                    'restaurantId': r['restaurant']['restaurantId'][0],
                    'name': r['restaurant']['name'][0]
                }
            } for r in reviews], None
        except Exception as e:
            return None, str(e)
        
        finally:
            db.close()

    @staticmethod
    def add_reply(review_id, owner_id, content):
        """商家回复评价"""
        try:
            # 创建回复顶点
            reply_id = str(uuid.uuid4())
            reply=db.g.addV('reply') \
              .property('replyId', reply_id) \
              .property('content', content) \
              .property('createdAt', datetime.now().isoformat()) \
              .next()
            
            owner=db.g.V().has('user', 'userId', owner_id).next()  # 唯一商家顶点
            assert owner, "用户不存在"
            review=db.g.V().has('review', 'reviewId', review_id).next()  # 唯一评价顶点
            assert review, "用户不存在"
            # 创建商家->回复关系
            db.g \
                   .addE('wrote') \
                   .from_(owner) \
                   .to(reply) \
                   .next()
            db.close()
            # 创建评价<-回复关系
            db.g \
                   .addE('has_reply') \
                   .from_(review)\
                   .to(reply) \
                   .next()
            
            return reply_id, None
        except StopIteration:
            return None, "商家或评价不存在"
        except Exception as e:
            return None, str(e)
        finally:
            db.close()

    @staticmethod
    def delete(review_id):
        """删除评价"""
        try:
            from utils.file_utils import delete_review_images  # 延迟导入避免循环依赖
            delete_review_images(review_id)  # 删除图片
           # 删除相关回复
            db.g.V().has('review', 'reviewId', review_id) \
                   .out('has_reply') \
                   .drop() \
                   .iterate()
            
            # 删除评价顶点
            db.g.V().has('review', 'reviewId', review_id) \
                   .drop() \
                   .iterate()
            
            return True, None
        except Exception as e:
            return False, str(e)
        finally:
            db.close()

    #添加图片函数
    @staticmethod
    def add_images(review_id, files=None):
        try:

            review=db.g.V().has('review', 'reviewId', review_id).next()  # 唯一评价顶点
            assert review, "评论不存在"
            
            saved_images = []
            if files:
                from utils.file_utils import save_review_images  # 延迟导入避免循环依赖
                saved_images = save_review_images(review_id, files)
                # 更新顶点属性
                db.g.V(review).property('images', saved_images).next()

            
            return saved_images, None
        except StopIteration:
            return None, "添加图片失败"
        except Exception as e:
            return None, str(e)
        finally:
            db.close()
    
    #指定函数
    @staticmethod
    def Pin(review_id):
        try:
            review=db.g.V().has('review', 'reviewId', review_id).next()  # 唯一评价顶点
            assert review, "评论不存在"
            data=db.g.V().has('review', 'reviewId', review_id).valueMap(True).next()
            print("fuck")
            print("data:", data['pin'][0])
            new_pin = False if data['pin'][0] else True # 切换置顶状态
            print("new_pin:", new_pin)
            db.g.V(review).property('pin', new_pin).next()

            
            return True, None
        except StopIteration:
            return False, "置顶失败"
        except Exception as e:
            return False, str(e)
        finally:
            db.close()
    
    #点赞函数函数
    @staticmethod
    def Like(review_id):
        try:
            review=db.g.V().has('review', 'reviewId', review_id).next()  # 唯一评价顶点
            assert review, "评论不存在"
            data=db.g.V().has('review', 'reviewId', review_id).valueMap(True).next()
            like=data['like'][0] #获取点赞数
            #print("like:", like)
            like+=1
            #print("new_like:", like)
            db.g.V(review).property('like',like).next()

            
            return like, None
        except StopIteration:
            return None, "置顶失败"
        except Exception as e:
            return None, str(e)
        finally:
            db.close()
    
    @staticmethod
    def dislike(review_id):
        try:
            review=db.g.V().has('review', 'reviewId', review_id).next()  # 唯一评价顶点
            assert review, "评论不存在"
            
            data=db.g.V(review).valueMap(True).next() #获取点赞数
            like=data['like'][0]  # 获取点赞数
            #print("like:", like)
            new_like=like-1 if like > 0 else 0  # 确保点赞数不为负
            #print("new_like:", new_like)
            db.g.V(review).property('like',new_like ).next()

            
            return new_like, None
        except StopIteration:
            return None, "置顶失败"
        except Exception as e:
            return None, str(e)
        finally:
            db.close()

    #点赞函数函数
    @staticmethod
    def get_like(review_id):
        try:
            review=db.g.V().has('review', 'reviewId', review_id).next()  # 唯一评价顶点
            assert review, "评论不存在"
            
            like=db.g.V(review).values('like').next() #获取点赞数
            assert like, "点赞数不存在"

            
            return like, None
        except StopIteration:
            return None, "置顶失败"
        except Exception as e:
            return None, str(e)
        finally:
            db.close()