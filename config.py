import os

class Config:
    SECRET_KEY = 'super-secret'
    JWT_SECRET_KEY = 'jwt-secret-string'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 当前 config.py 所在目录
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'tomo.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False