from rest_framework import serializers
from analyses.models import AnalysisTask, Violation
from users.serializers import UserSerializer
from questionnaires.serializers import QuestionnaireSerializer

class AnalysisTaskSerializer(serializers.ModelSerializer):
    analyst_id = UserSerializer(read_only=True)
    questionnaire_id = QuestionnaireSerializer(read_only=True)

    class Meta:
        model = AnalysisTask
        fields = ['id', 'analyst_id', 'questionnaire_id', 'task_name', 'status', 'export_format', 'result_url', 'created_at', 'updated_at']

class AnalysisTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisTask
        fields = ['questionnaire_id', 'task_name', 'export_format']

class ViolationSerializer(serializers.ModelSerializer):
    questionnaire_id = QuestionnaireSerializer(read_only=True)
    respondent_id = UserSerializer(read_only=True)
    processed_by = UserSerializer(read_only=True)

    class Meta:
        model = Violation
        fields = ['id', 'questionnaire_id', 'respondent_id', 'ip_address', 'violation_type', 'description', 'status', 'processed_by', 'processed_at', 'created_at', 'updated_at']

class ViolationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Violation
        fields = ['questionnaire_id', 'respondent_id', 'ip_address', 'violation_type', 'description']
