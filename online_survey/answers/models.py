from django.db import models
from django.utils import timezone
from users.models import User
from questionnaires.models import Questionnaire, Question

class Response(models.Model):
    id = models.BigAutoField(primary_key=True)
    questionnaire_id = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, db_column='questionnaire_id')
    respondent_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='respondent_id')
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    temp_data = models.JSONField(null=True, blank=True)  # 暂存数据
    is_completed = models.SmallIntegerField(default=0)  # 是否完成
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'response'

    def __str__(self):
        return f"Response {self.id} for Questionnaire {self.questionnaire_id.title}"

class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    response_id = models.ForeignKey(Response, on_delete=models.CASCADE, db_column='response_id')
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, db_column='question_id')
    value = models.JSONField(null=False)  # 答案内容（JSON格式）
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'answer'

    def __str__(self):
        return f"Answer {self.id} for Question {self.question_id.content}"
