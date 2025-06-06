from flask import Flask
from config import Config
from app.extensions import db  # 导入数据库实例
from app.extensions import jwt  # 导入JWT实例

def create_app(config_class=Config):
    """应用工厂函数"""
    app = Flask(__name__, static_folder='static', template_folder='templates')  # 添加template_folder
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    
    # 注册蓝图
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.restaurant import restaurant_bp
    from app.routes.review import review_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    #app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(user_bp) # 取消url_prefix以便于访问
    app.register_blueprint(restaurant_bp, url_prefix='/api/restaurants')
    app.register_blueprint(review_bp, url_prefix='/api/reviews')

    return app