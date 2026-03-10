from django.test import TestCase
from users.models import User
from users.serializers import UserCreateSerializer

class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        """测试用户注册功能是否正常工作"""
        # 准备测试数据
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'role': 'respondent'
        }
        
        # 创建序列化器
        serializer = UserCreateSerializer(data=data)
        
        # 验证数据
        self.assertTrue(serializer.is_valid())
        
        # 保存用户
        user = serializer.save()
        
        # 验证用户是否成功创建
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'respondent')
        
        # 验证密码是否正确存储（密码应该是哈希值，不是明文）
        self.assertNotEqual(user.password, 'testpassword123')
        
        # 验证用户是否可以通过密码认证
        self.assertTrue(user.check_password('testpassword123'))
