# 开发笔记

## 文件目录结构
food-review-demo/
├── app/                      # 主应用目录
│   ├── __init__.py           # 应用工厂函数和初始化
│   ├── models/               # 数据模型和Gremlin操作  
│   │   ├── __init__.py
│   │   ├── user.py           # 用户相关操作
│   │   ├── restaurant.py     # 餐厅相关操作
│   │   ├── review.py         # 评价相关操作
│   │   └── friendship.py     # 好友关系相关操作
│   ├── routes/               # 路由和视图函数
│   │   ├── __init__.py
│   │   ├── auth.py           # 认证相关路由
│   │   ├── user.py           # 用户相关路由
│   │   ├── restaurant.py     # 餐厅相关路由
│   │   └── review.py         # 评价相关路由
│   ├── static/               # 静态文件
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/            # HTML模板
│   │   ├── base.html         # 基础模板
│   │   ├── auth/             # 认证相关模板
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── restaurant/       # 餐厅相关模板
│   │   │   ├── list.html
│   │   │   ├── detail.html
│   │   │   └── add.html
│   │   ├── user/            # 用户相关模板
│   │   │   ├── profile.html
│   │   │   └── friends.html
│   │   └── review/          # 评价相关模板
│   │       └── list.html
│   ├── utils/                # 工具函数
│   │   ├── __init__.py
│   │   ├── auth.py           # 认证工具
│   │   └── decorators.py     # 装饰器
│   └── config.py             # 应用配置
├── tests/                    # 测试目录
│   ├── __init__.py
│   ├── test_models/
│   └── test_routes/
├── migrations/               # 数据库迁移脚本(如果需要),暂时没有
├── venv/                     # Python虚拟环境(不应提交到版本控制)
├── .env                      # 环境变量
├── .gitignore                # Git忽略规则
├── requirements.txt          # Python依赖
├── README.md                 # 项目说明
└── run.py                    # 网站启动文件
└── tomo.bat                    # 应用启动脚本 一般是用这个去更新你在开发中新添加的python模块，并且每次都是用这个去打开网站，然后用跳出来的地址去打开网站

## github协同开发说明

### 首先是