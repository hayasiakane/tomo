import sys
import os
from flask import current_app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(sys.path)  # 应输出包含 app 目录的路径
from utils.file_utils import save_user_images
print(save_user_images)  # 应输出函数对象