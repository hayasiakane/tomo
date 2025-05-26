import os
import uuid
from werkzeug.utils import secure_filename
import shutil


REVIEW_IMAGE_DIR='./data/images/review'  # 替换为实际路径
USER_IMAGE_DIR = './data/images/user'  # 替换为实际路径
RESTAURANT_IMAGE_DIR = './data/images/restaurant'  # 替换为实际路径
ALLOWED_EXTENSIONS= {'png', 'jpg', 'jpeg', 'gif'}  # 允许的图片扩展名
log_flag = False

if log_flag:
    from flask import current_app 

def save_review_images(review_id, files):
    """保存评论图片到对应目录"""
    if not files or 'images' not in files:
        return []
    
    image_dir = os.path.join(REVIEW_IMAGE_DIR, review_id)
    os.makedirs(image_dir, exist_ok=True)  # 创建目录
    
    saved_files = []
    for file in files.getlist('images'):
        if file.filename == '':
            continue
        if allowed_file(file.filename):
            # 生成唯一文件名：uuid + 原始后缀
            ext = os.path.splitext(file.filename)[1]
            filename = secure_filename(f"{uuid.uuid4().hex}{ext}")
            file.save(os.path.join(image_dir, filename))
            saved_files.append(filename)
            if log_flag:
                current_app.logger.info(f"Saved review image: {filename} at {image_dir}")
        else:
            if log_flag:
                current_app.logger.warning(f"File {file.filename} is not allowed.")
    return saved_files

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delete_review_images(review_id):
    """删除评论对应的图片目录"""
    image_dir = os.path.join(REVIEW_IMAGE_DIR, review_id)
    if os.path.exists(image_dir):
        shutil.rmtree(image_dir)
        if log_flag:
            current_app.logger.info(f"Deleted review images at {image_dir}")
    else:
        if log_flag:
            current_app.logger.warning(f"Review image path {image_dir} does not exist.")
    return True

def save_user_images(user_id, files):
    """保存评论图片到对应目录"""
    if not files or 'images' not in files:
        return []
    
    image_dir = os.path.join(USER_IMAGE_DIR, user_id)
    os.makedirs(image_dir, exist_ok=True)  # 创建目录
    
    saved_files = []
    #request.files.getlist('images') 获取上传的文件列表
    for file in files.getlist('images'):
        if file.filename == '':
            continue
        if allowed_file(file.filename):
            # 生成唯一文件名：uuid + 原始后缀
            ext = os.path.splitext(file.filename)[1]
            filename = secure_filename(f"{uuid.uuid4().hex}{ext}")
            file.save(os.path.join(image_dir, filename))
            saved_files.append(filename)
            if log_flag:
                current_app.logger.info(f"Saved user image: {filename} at {image_dir}")
        else:
            if log_flag:
                current_app.logger.warning(f"File {file.filename} is not allowed.")
    
    return saved_files

def delete_user_images(user_id):
    """删除对应的用户图片目录"""
    image_dir = os.path.join(USER_IMAGE_DIR, user_id)
    if os.path.exists(image_dir):
        shutil.rmtree(image_dir)
        if log_flag:
            current_app.logger.info(f"Deleted user images at {image_dir}")
    else:
        if log_flag:
            current_app.logger.warning(f"User image path {image_dir} does not exist.")

def save_restaurant_images(restaurant_id, files):
    """保存餐厅图片到对应目录"""
    if not files or 'images' not in files:
        return []
    
    image_dir = os.path.join(RESTAURANT_IMAGE_DIR, restaurant_id)
    os.makedirs(image_dir, exist_ok=True)  # 创建目录
    
    saved_files = []
    # request.files.getlist('images') 获取上传的文件列表
    for file in files.getlist('images'):
        if file.filename == '':
            continue
        if allowed_file(file.filename):
            # 生成唯一文件名：uuid + 原始后缀
            ext = os.path.splitext(file.filename)[1]
            filename = secure_filename(f"{uuid.uuid4().hex}{ext}")
            file.save(os.path.join(image_dir, filename))
            saved_files.append(filename)
            if log_flag:
                current_app.logger.info(f"Saved restaurant image: {filename} at {image_dir}")
        else:
            if log_flag:
                current_app.logger.warning(f"File {file.filename} is not allowed.")
    return saved_files

def delete_restaurant_images(restaurant_id):
    """删除餐厅图片目录"""
    image_dir = os.path.join(RESTAURANT_IMAGE_DIR, restaurant_id)
    if os.path.exists(image_dir):
        shutil.rmtree(image_dir)
        if log_flag:
            current_app.logger.info(f"Deleted restaurant images at {image_dir}")
    else:
        if log_flag:   
            current_app.logger.warning(f"Restaurant image path {image_dir} does not exist.")

def delete_single_image(res_id,filename):
    image_path= os.path.join(RESTAURANT_IMAGE_DIR, res_id, filename)
    """删除单张图片"""
    if os.path.isfile(image_path):
        os.remove(image_path)
        if log_flag:
            current_app.logger.info(f"Deleted image at {image_path}")
    else:
        if log_flag:
            current_app.logger.warning(f"Image path {image_path} does not exist.")