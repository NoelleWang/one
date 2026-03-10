import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_survey.settings')
django.setup()

from users.models import User

# 删除现有的admin用户（如果存在）
try:
    existing_user = User.objects.get(email='admin@example.com')
    existing_user.delete()
    print('已删除现有admin用户')
except User.DoesNotExist:
    print('没有找到admin用户')

# 创建超级用户
user = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123'
)

print('超级用户创建成功！')
print(f'用户名: {user.username}')
print(f'邮箱: {user.email}')
print(f'角色: {user.role}')
