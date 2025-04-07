import os
from dotenv import load_dotenv

# 加载环境变量（如果有）
load_dotenv()

class Config:
    # 基础Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
    
    # Gremlin数据库配置（无密码版本）
    GREMLIN_SERVER_URL = os.getenv('GREMLIN_SERVER_URL', 'ws://localhost:8182/gremlin')
    
    # 调试设置
    DEBUG = True
    
    # 其他开发专用配置
    TEMPLATES_AUTO_RELOAD = True  # 模板自动重载