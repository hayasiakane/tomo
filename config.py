import os
from dotenv import load_dotenv

# 加载环境变量（如果有）
load_dotenv()

class Config:
    # 基础Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
    
    # Gremlin数据库配置（无密码版本）
    GREMLIN_SERVER_URL = os.getenv('GREMLIN_SERVER_URL', 'ws://localhost:8182/gremlin')
    
    # 图片存储根目录（默认值：项目根目录下的 data/images）
    REVIEW_IMAGE_DIR = os.getenv('REVIEW_IMAGE_DIR', os.path.abspath(REVIEW_IMAGE_DIR))
    
    # 用户存储根目录（默认值：项目根目录下的 data/images）
    USER_IMAGE_DIR = os.getenv('USER_IMAGE_DIR', os.path.abspath('./data/images/user'))
    # 餐厅图片存储根目录（默认值：项目根目录下的 data/images）
    RESTAURANT_IMAGE_DIR = os.getenv('RESTAURANT_IMAGE_DIR', os.path.abspath('./data/images/restaurant'))
    # 允许的图片扩展名（安全限制）
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # 调试设置
    DEBUG = True
    
    # 其他开发专用配置
    TEMPLATES_AUTO_RELOAD = True  # 模板自动重载

    @classmethod
    def ensure_dirs(cls):
        """确保必要的文件目录存在（可在应用启动时调用）"""
        os.makedirs(cls.REVIEW_IMAGE_DIR, exist_ok=True)  # 创建图片存储目录