```bash
venv\scripts\activate # 进入虚拟环境
python run.py # 运行网站
```

首页功能：\\
商家和用户有区别，可以点击不同菜系跳转到餐厅页面进行筛选 \\
获取评价数最多的四个热门餐厅进行展示，可以点击用户头像进入其主页 \\
获取最新的两个评价进行展示 \\

餐厅页面：\\ 
可以按照搜索词或菜系进行筛选 \\
商家的页面有添加餐厅按钮 \\

评价页面：\\
按照搜索、评分、新旧筛选 \\

好友页面：\\
展示自己关注的用户 \\

添加餐厅页面：\\
填写餐厅信息添加 \\

餐厅详情页面：\\
展示详细信息 \\
写评价 \\
商户自己的餐厅页面可以进行添加封面图 \\

个人资料页面：\\
展示个人信息 \\
编辑信息 \\

我的餐厅页面：\\
展示自己的餐厅，可以进行添加展示图(详情页的图片，不是封面图)

好友主页：\\
查看其信息 \\
进行关注或取关 \\
展示其餐厅和评价，点击卡片可进入详情页 \\




## github 协同开发说明

### 分支策略

. 主分支：main（受保护，禁止直接推送）。

. 开发分支：dev（集成分支，测试通过后合并到 main）。

. 功能分支：feature/功能名（如 feature/user-auth）。

### 初始化本地仓库

1. 因为是私人库，所以要先告诉 git 你是谁(以后每次提交代码都需要这个步骤)

```bash
   git config --global user.name "你的用户名"
   git config --global user.email "你的邮箱"
```

2.  拉取源文件
    `git clone https://github.com/hayasiakane/tomo.git`


### 提交过程

#### Tips:在关联好库之后，可以用 vscode 去查看分支

1.  关联远程代码库
    `git remote add origin https://github.com/hayasiakane/tomo.git`

2.  拉取最新代码
    `git pull origin dev`
    或者
    `git pull origin main`

3.  开发完成后提交

```bash
   git add .
   git commit -m "feat: 添加用户登录功能"
```

4. 推送到远程
   `git push origin 分支名（一般先提交到feature/你的功能名）`

5. 在 GitHub 创建 Pull Request（PR）到 `dev` 分支

### 团队协作时定期同步

```bash
git fetch origin #获取远程更新
git merge origin/main #合并到本地
```

### 常见问题说明

1.  如果你浏览器可以登上 github，可是拉取或者提交文件时显示你连不上 github，可以尝试以下做法
    1. 查看你设置里网络代理的地址和端口，然后在你准备提交文件的 cmd 窗口里运行以下命令

```bash
         set HTTP_PROXY=http://地址:端口
         set HTTPS_PROXY=http://地址:端口
```
