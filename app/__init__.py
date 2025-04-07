from flask import Flask
from config import Config
from .models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化数据库
    db.init_app(app)
    
    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.restaurant import restaurant_bp
    from app.routes.review import review_bp
    from app.routes.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(main_bp)
    
    return app

#config还是要好好研究一下，如何创建一个带密码的graphDB?config需要什么？怎么用？