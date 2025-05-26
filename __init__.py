from flask import Flask
from .config import Config
from app.models import db  # 导入数据库实例
import logging  #导入日志功能
from logging.handlers import RotatingFileHandler

def create_app(config_class=Config):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config_class)  # 加载配置
    
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
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(restaurant_bp, url_prefix='/api/restaurants')
    app.register_blueprint(review_bp, url_prefix='/api/reviews')

    #设置日志
    # 配置日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # 设置日志文件路径和大小轮转（例如：10MB一个文件，保留5个备份）
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=10*1024*1024, 
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # 将处理器添加到 Flask 的日志记录器中
    app.logger.addHandler(file_handler)

    # 设置日志级别（根据环境变量动态调整）
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

    # 可选：同时输出到控制台
    if app.debug:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)
    
    return app