from django.db import models
from django.utils import timezone
from users.models import User

class Template(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True)
    content = models.JSONField(null=False)  # 模板结构（包含题目、选项、逻辑等JSON）
    category = models.CharField(max_length=50, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'template'

    def __str__(self):
        return self.name

class Questionnaire(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '发布中'),
        ('closed', '已关闭'),
    )

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='creator_id')
    template_id = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True, db_column='template_id')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    max_responses = models.IntegerField(default=0)  # 最大填写次数（0表示不限）
    ip_limit = models.SmallIntegerField(default=0)  # 是否限制IP重复填写（1-是，0-否）
    allow_anonymous = models.SmallIntegerField(default=0)  # 是否允许匿名填写（1-是，0-否）
    is_public_result = models.SmallIntegerField(default=0)  # 结果是否公开给填写者查看
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'questionnaire'

    def __str__(self):
        return self.title

class Question(models.Model):
    TYPE_CHOICES = (
        ('single', '单选'),
        ('multiple', '多选'),
        ('text', '填空'),
        ('scale', '量表'),
    )

    id = models.BigAutoField(primary_key=True)
    questionnaire_id = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, db_column='questionnaire_id')
    content = models.TextField(null=False)  # 题目内容
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=False)
    options = models.JSONField(null=True, blank=True)  # 选项（JSON格式）
    required = models.SmallIntegerField(default=0)  # 是否必填（1-是，0-否）
    order = models.IntegerField(default=0)  # 题目顺序
    logic_rules = models.JSONField(null=True, blank=True)  # 跳转逻辑
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'question'
        ordering = ['order']

    def __str__(self):
        return self.content
