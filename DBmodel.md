# TOMOT数据库模型

## 类描述

### User
1. 属性
    . userId （用户Id） <br>自动添加，不需要管</br>
    . name   （用户名）
    . email  （邮箱）
    . password  （密码） <br>正常传递数字密码就行，哈希加密已在数据模型中实现</br>
    . type "regular:普通用户； business:经营者"
    . createdAt (创建时间)  <br>自动添加，不需要管</br>

2. 函数
    1. 导入类
        `from app.models.user import User`

    2. 注册函数:register
        1. 语句：
            `User.register(name,email,password,user_type) #userid已在函数内自动生成，user_type用网页提交的`
        2. 作用：
            . 实现注册
        3. 返回内容
            `return user_id(用户id), None(状态码)`
    
    3. 认证函数：authenticate
        1. 语句：
        `User.authenticate(email, password)`
        2. 作用
            1. 登录
        3. 返回内容
        ```
        return {
                'user_id': result[0]['user_id'],
                'name': result[0]['name']
            }(json), None(状态码)
        ```
    
    4. ID获取用户信息：get_by_id
        1. 语句：
            `User.get_by_id(user_id)`
        2. 作用
            1. 获取用户信息
        3. 返回内容
        ```
            return {
                'userId': user['userId'][0],
                'name': user['name'][0],
                'email': user['email'][0],
                'type': user['type'][0],
                'createdAt': user['createdAt'][0]
            }(包含所有用户内容的json), None
        ```
    
    5. email获取用户信息：get_by_email
        1. 语句：
            `User.get_by_email(user_email)`
        2. 其余同上

    6. name获取用户信息：get_by_name
        1. 语句：
            `User.get_by_name(user_name)`
        2. 其余同上
    
    7. 添加好友： add_friend:
        1. 语句：
            `User.add(user_id,friend_id)`
        2. 作用
            1. 添加好友
        3. 返回内容:布尔值
    
    8. 获取好友列表：get_friends
        1. 语句：
            `User.get_friends(user_id)`
        2. 作用
            1. 获取该用户所有的好友列表
        3. 返回内容：包含所有的好友的id,name，email内容的json
            ```
            return [{
                'userId': f['userId'][0],
                'name': f['name'][0],
                'email': f['email'][0]
            } for f in friends], None
            ```
    
    9. 移除好友：remove_friend
        1. 语句
            `User.remove_friend(user_id,friend_id)`
        2. 作用
            1. 删除好友
        3. 返回内容：布尔值
    
    10. 根据属性查询用户：get(attribute='userId', value=None)
     1.语句
     `User.get('name',user_name)`

     2. 其余与最上面的获取函数一致

### restaurant
1. 属性
    1. restaurantId (餐厅id)  <br>自动添加，不需要管</br>
    2. name (餐厅名字)
    3. address (餐厅地址)
    4. cuisine (菜单，先创建json对象再传递进去)
    5. description (餐厅描述)
    6. createdAt (添加时间) <br>自动添加，不需要管</br>

2. 函数
    1. 导入类
        `from app.models.restaurant import Restaurant`
    
    2. 创建：create
        1. 语句

            ```Python
            user_id = request.cookies.get('user_id') #获取用户id
            data = request.get_json()  #获取注册数据
            
            restaurant_id, error = Restaurant.create(
                owner_id=user_id,
                name=data.get('name'),
                address=data.get('address'),
                cuisine=data.get('cuisine', ''),
                description=data.get('description', '')
            )
            ```
        
        2. 作用：添加餐厅

        3.返回：餐厅id及错误信息
        `return restaurant_id, None`
    
    3. 通过餐厅id获取餐厅信息： get_by_id(restaurant_id)
        1. 语句 
        `Restaurant.get_by_id(restaurant_id)`

        2. 返回：餐厅全部信息及评论数量及错误信息
        ```Python
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
        ```
    
    4. 根据属性获取餐厅信息：get(attribute='restaurantId', value=None)，把属性名的字符串及值赋值给get参数即可，默认是用restaurantId查询

        1.语句 
        `Restaurant.get('name',name)`

        2.返回与上面一致