# 开发笔记

## 文件目录结构
food-review-demo/
├── app/                      # 主应用目录
│   ├── __init__.py           # 应用工厂函数和初始化
│   ├── models/               # 数据模型和Gremlin操作   负责人1：hayasiakane
│   │   ├── __init__.py
│   │   ├── user.py           # 用户相关操作
│   │   ├── restaurant.py     # 餐厅相关操作
│   │   ├── review.py         # 评价相关操作
│   │   └── friendship.py     # 好友关系相关操作
│   ├── routes/               # 路由和视图函数
│   │   ├── __init__.py
│   │   ├── auth.py           # 认证相关路由    负责人2：樊
│   │   ├── user.py           # 用户相关路由    负责人2：樊
│   │   ├── restaurant.py     # 餐厅相关路由    负责人3：季
│   │   └── review.py         # 评价相关路由    负责人4：钟
│   ├── static/               # 静态文件
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/            # HTML模板
│   │   ├── base.html         # 基础模板     负责人5：王
│   │   ├── auth/             # 认证相关模板   负责人5：王
│   │   │   ├── login.html   
│   │   │   └── register.html
│   │   ├── restaurant/       # 餐厅相关模板   负责人6：雷
│   │   │   ├── list.html
│   │   │   ├── detail.html
│   │   │   └── add.html
│   │   ├── user/            # 用户相关模板    负责人7：叶婷
│   │   │   ├── profile.html
│   │   │   └── friends.html
│   │   └── review/          # 评价相关模板    负责人6：雷
│   │       └── myreview.html
│   ├── utils/                # 工具函数
│   │   ├── __init__.py
│   │   ├── auth.py           # 认证工具
│   │   └── decorators.py     # 装饰器
│   └── config.py             # 应用配置
├── tests/                    # 测试目录 目前没有
│   ├── __init__.py
│   ├── test_models/
│   └── test_routes/
├── migrations/               # 数据库迁移脚本(如果需要),暂时没有
├── venv/                     # Python虚拟环境(不应提交到版本控制)
├── .env                      # 环境变量
├── .gitignore                # Git忽略规则  当前文件夹你有什么不想被提交上去的可以写进去
├── requirements.txt          # Python依赖 开发过程中有用到什么新的库也要即时添加进去
├── README.md                 # 项目说明
└── run.py                    # 网站启动文件
└── config.py                    # 配置文件
└──init.py                    # 项目初始化文件
└── tomo.bat                    # 应用启动脚本 一般是用这个去更新你在开发中新添加的python模块，并且每次都是用这个去打开网站，然后用跳出来的地址去打开网站

## github协同开发说明


### 分支策略
   . 主分支：main（受保护，禁止直接推送）。

   . 开发分支：dev（集成分支，测试通过后合并到 main）。

   . 功能分支：feature/功能名（如 feature/user-auth）。

### 初始化本地仓库
  1. 因为是私人库，所以要先告诉git你是谁(以后每次提交代码都需要这个步骤)
   ```bash
      git config --global user.name "你的用户名"
      git config --global user.email "你的邮箱"
   ```

   2. 拉取源文件
  `git clone https://github.com/hayasiakane/tomo.git`

### 没下载java的要下载一下，推荐JDK8这个长期支持版本

### 提交过程
#### Tips:在关联好库之后，可以用vscode去查看分支
   1. 关联远程代码库
   `git remote add origin https://github.com/hayasiakane/tomo.git`

   2. 拉取最新代码
     `git pull origin dev`
     或者
     `git pull origin main`


   3. 开发完成后提交
   ```
      git add .
      git commit -m "feat: 添加用户登录功能" 
      ```

 4. 推送到远程
  `git push origin 分支名（一般先提交到feature/你的功能名）`

  5. 在 GitHub 创建 Pull Request（PR）到 `dev` 分支


### 团队协作时定期同步

  ```
   git fetch origin   #获取远程更新
   git merge origin/main   #合并到本地 
```

### 常见问题说明
   1. 如果你浏览器可以登上github，可是拉取或者提交文件时显示你连不上github，可以尝试以下做法
      1. 查看你设置里网络代理的地址和端口，然后在你准备提交文件的cmd窗口里运行以下命令

      ```bash
         set HTTP_PROXY=http://地址:端口
         set HTTPS_PROXY=http://地址:端口
      ```