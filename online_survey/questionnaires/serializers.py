from rest_framework import serializers
from questionnaires.models import Template, Questionnaire, Question
from users.serializers import UserSerializer

class TemplateSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Template
        fields = ['id', 'name', 'description', 'content', 'category', 'created_by', 'created_at', 'updated_at']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'content', 'type', 'options', 'required', 'order', 'logic_rules', 'created_at', 'updated_at']

class QuestionnaireSerializer(serializers.ModelSerializer):
    creator_id = UserSerializer(read_only=True)
    template_id = TemplateSerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Questionnaire
        fields = ['id', 'title', 'description', 'creator_id', 'template_id', 'status', 'start_time', 'end_time', 'max_responses', 'ip_limit', 'allow_anonymous', 'is_public_result', 'questions', 'created_at', 'updated_at']

class QuestionnaireCreateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Questionnaire
        fields = ['title', 'description', 'template_id', 'status', 'start_time', 'end_time', 'max_responses', 'ip_limit', 'allow_anonymous', 'is_public_result', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        questionnaire = Questionnaire.objects.create(**validated_data)
        
        for i, question_data in enumerate(questions_data):
            question_data['questionnaire_id'] = questionnaire
            question_data['order'] = i
            Question.objects.create(**question_data)
        
        return questionnaire

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', None)
        instance = super().update(instance, validated_data)
        
        if questions_data is not None:
            # 先删除旧的题目
            instance.question_set.all().delete()
            # 创建新的题目
            for i, question_data in enumerate(questions_data):
                question_data['questionnaire_id'] = instance
                question_data['order'] = i
                Question.objects.create(**question_data)
        
        return instance
