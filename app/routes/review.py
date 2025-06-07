from flask import Blueprint, request, jsonify
from app.models.review import review
from app.models.user import User
from app.utils.decorators import login_required
from app.extensions import db
from app.models.restaurant import Restaurant

review_bp = Blueprint('review', __name__)

@review_bp.route('/add/<restaurant_id>', methods=['POST'])
@login_required
def api_add_review(restaurant_id):

    data = request.get_json()  # 避免重复获取

    # 创建新评价
    review_text = data.get('content')
    rating = data.get('rating')
    userId = data.get('userId')
    # 打印rating的类型和内容
    # print(f"Rating type: {type(rating)}, value: {rating}")
    rating = int(rating) if rating is not None else None

    if not review_text or not rating:
        return {'error': 'Missing required fields'}, 400
    
    # 1. 先创建评价记录
    new_review = review(
        restaurantId=restaurant_id,
        userId=userId,
        content=review_text,
        rating=rating
    )
    
    try:
        # 2. 提交评价到数据库
        db.session.add(new_review)
        db.session.commit()
        
        # 3. 更新餐厅的 review_count 和 average_rating（优化版）
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return {'error': 'Restaurant not found'}, 404
        
        # 直接更新 review_count（+1）
        restaurant.review_count += 1
        
        # 计算新的 average_rating（避免全表查询）
        # 新平均分 = (原总分 + 新评分) / (原评价数 + 1)
        if restaurant.review_count == 1:
            # 如果是第一条评价，直接赋值
            restaurant.average_rating = rating
        else:
            # 否则计算新的平均值
            restaurant.average_rating = round(
                (restaurant.average_rating * (restaurant.review_count - 1) + rating) / restaurant.review_count,
                1  # 保留1位小数
            )
        
        db.session.commit()
        
        return {'message': 'Review added successfully'}, 201
    
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@review_bp.route('/get/<restaurant_id>', methods=['GET'])
def api_get_reviews(restaurant_id):
    page = int(request.args.get('page', 1))  # 当前页
    per_page = int(request.args.get('per_page', 5))  # 每页几条
    sort = request.args.get('sort', 'latest')  # 排序方式

    # 构造查询对象
    query = review.query.filter_by(restaurantId=restaurant_id)

    # 应用排序规则
    if sort == 'lowest':
        query = query.order_by(review.rating.asc())
    elif sort == 'highest':
        query = query.order_by(review.rating.desc())
    else:  # 默认是 latest
        query = query.order_by(review.createdAt.desc())

    # 总数与分页
    total_reviews = query.count()
    reviews = query.offset((page - 1) * per_page).limit(per_page).all()

    reviews_data = [{
        'reviewId': r.reviewId,
        'userId': r.userId,
        'content': r.content,
        'rating': r.rating,
        'createdAt': r.createdAt.isoformat()
    } for r in reviews]

    return {
        'reviews': reviews_data,
        'page': page,
        'per_page': per_page,
        'total': total_reviews,
        'total_pages': (total_reviews + per_page - 1) // per_page
    }, 200




@review_bp.route('/display-all/<user_id>', methods=['GET'])
def api_display_all_reviews(user_id):
    search = request.args.get('search', '').strip()
    rating = request.args.get('rating', '').strip()
    sort = request.args.get('sort', '').strip()  # 排序方式
    # print(f"Search: {search}, Rating: {rating}, Sort: {sort}")
    # 构造查询条件
    query = review.query

    if search:
        query = query.filter(review.content.ilike(f"%{search}%"))
    
    if rating:
        try:
            rating = int(rating)
            query = query.filter(review.rating == rating)
        except ValueError:
            return {'message': 'Invalid rating value'}, 400

    if sort == 'newest':
        query = query.order_by(review.createdAt.desc())
    elif sort == 'oldest':
        query = query.order_by(review.createdAt.asc())

    # 执行查询
    reviews = query.filter_by(userId=user_id).all()
    if not reviews:
        return {'message': 'No reviews found for this user'}, 404
    reviews_data = [{
        'reviewId': review.reviewId,
        'restaurantId': review.restaurantId,
        'content': review.content,
        'rating': review.rating,
        'createdAt': review.createdAt.isoformat()
    } for review in reviews]
    return {'reviews': reviews_data}, 200

import traceback

@review_bp.route('/delete/<review_id>', methods=['DELETE'])
def api_delete_review(review_id):
    try:
        deleted_review = review.query.get(review_id)
        if not deleted_review:
            return {'error': 'Review not found'}, 404

        restaurant = Restaurant.query.get(deleted_review.restaurantId)
        if not restaurant:
            return {'error': '关联餐厅不存在'}, 404

        # 删除评论
        db.session.delete(deleted_review)
        db.session.commit()

        # 重新统计
        remaining_reviews = review.query.filter_by(restaurantId=restaurant.restaurantId).all()
        restaurant.review_count = len(remaining_reviews)
        restaurant.average_rating = (
            round(sum(r.rating for r in remaining_reviews) / len(remaining_reviews), 2)
            if remaining_reviews else 0.0
        )
        db.session.commit()

        return {'message': 'Review deleted and restaurant updated successfully'}, 200

    except Exception as e:
        db.session.rollback()
        print("❌ 删除评论失败：", traceback.format_exc())
        return {'error': str(e)}, 500


@review_bp.route('/latest', methods=['GET'])
def api_get_latest_reviews():
    try:
        reviews = (
            review.query.filter(review.restaurantId.isnot(None))
            .order_by(review.createdAt.desc())
            .limit(2)
            .all()
        )

        # 批量查询避免N+1问题
        user_ids = {r.userId for r in reviews}
        restaurant_ids = {r.restaurantId for r in reviews}

        users = {u.userId: u for u in User.query.filter(User.userId.in_(user_ids)).all()}
        restaurants = {r.restaurantId: r for r in Restaurant.query.filter(Restaurant.restaurantId.in_(restaurant_ids)).all()}

        result = []
        for r in reviews:
            user = users.get(r.userId)
            restaurant = restaurants.get(r.restaurantId)
            result.append({
                "reviewId": r.reviewId,
                "content": r.content,
                "rating": r.rating,
                "createdAt": r.createdAt.isoformat(),
                "userId": r.userId,
                "restaurantId": r.restaurantId,
                "restaurantName": restaurant.name if restaurant else "Unknown",
                "userName": user.name if user else "Unknown",
                "userImage": user.image if user and user.image else None
            })

        return jsonify({"reviews": result}), 200

    except Exception as e:
        print("❌ 获取最新评论失败：", e)
        return jsonify({"error": str(e)}), 500
