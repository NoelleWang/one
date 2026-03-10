from django.db import models
from django.utils import timezone
from users.models import User
from questionnaires.models import Questionnaire

class AnalysisTask(models.Model):
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    )

    id = models.BigAutoField(primary_key=True)
    analyst_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='analyst_id')
    questionnaire_id = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, db_column='questionnaire_id')
    task_name = models.CharField(max_length=200, null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=False, default='pending')
    export_format = models.CharField(max_length=20, null=False)  # Excel/SPSS
    result_url = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analysis_task'

    def __str__(self):
        return self.task_name

class Violation(models.Model):
    id = models.BigAutoField(primary_key=True)
    questionnaire_id = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, db_column='questionnaire_id')
    respondent_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='respondent_id')
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    violation_type = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')  # pending, processed
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_violations', db_column='processed_by')
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'violation'

    def __str__(self):
        return f"Violation {self.id} - {self.violation_type}"
