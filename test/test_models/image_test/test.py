import os
import unittest
from werkzeug.datastructures import FileStorage
from your_app import app, db
from models import Review  # 替换为你的实际模块路径

class TestImageUpload(unittest.TestCase):
    def setUp(self):
        # 初始化测试环境
        app.config['TESTING'] = True
        app.config['REVIEW_IMAGE_DIR'] = './tests/temp_images'  # 使用临时目录
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        # 清理测试数据
        db.session.remove()
        db.drop_all()
        # 删除测试生成的图片目录
        if os.path.exists(app.config['REVIEW_IMAGE_DIR']):
            shutil.rmtree(app.config['REVIEW_IMAGE_DIR'])

    def test_create_review_with_images(self):
        # 模拟文件上传
        test_images = [
            FileStorage(
                stream=open('tests/images/test1.jpg', 'rb'),
                filename='test1.jpg'
            ),
            FileStorage(
                stream=open('tests/images/test2.png', 'rb'),
                filename='test2.png'
            )
        ]

        # 构造 files 字典（与前端上传的字段名一致）
        files = {'images': test_images}

        # 调用创建方法
        review_id, error = Review.create(
            user_id='test_user_123',
            restaurant_id='test_restaurant_456',
            content='测试评价内容',
            rating=4,
            files=files
        )

        # 验证是否成功
        self.assertIsNone(error)
        self.assertIsNotNone(review_id)

        # 检查图片是否保存
        target_dir = os.path.join(app.config['REVIEW_IMAGE_DIR'], review_id)
        self.assertTrue(os.path.exists(target_dir))
        saved_files = os.listdir(target_dir)
        self.assertEqual(len(saved_files), 2)  # 应保存两张图片

        # 验证文件名格式（UUID + 原扩展名）
        for filename in saved_files:
            self.assertRegex(filename, r'^[0-9a-f]{32}\.(jpg|png)$')