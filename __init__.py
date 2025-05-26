from flask import Flask
from .config import Config
from app.models import db  # 导入数据库实例

def create_app(config_class=Config):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化数据库
    db.init_app(app)
    
    # 注册蓝图
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.restaurant import restaurant_bp
    from app.routes.review import review_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    #app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(user_bp)
    app.register_blueprint(restaurant_bp, url_prefix='/api/restaurants')
    app.register_blueprint(review_bp, url_prefix='/api/reviews')
    
    return app