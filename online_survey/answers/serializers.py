from rest_framework import serializers
from answers.models import Response, Answer
from questionnaires.serializers import QuestionnaireSerializer, QuestionSerializer
from users.serializers import UserSerializer

class AnswerSerializer(serializers.ModelSerializer):
    question_id = QuestionSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'question_id', 'value', 'created_at']

class ResponseSerializer(serializers.ModelSerializer):
    questionnaire_id = QuestionnaireSerializer(read_only=True)
    respondent_id = UserSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Response
        fields = ['id', 'questionnaire_id', 'respondent_id', 'ip_address', 'temp_data', 'is_completed', 'answers', 'created_at', 'updated_at']

class ResponseCreateSerializer(serializers.ModelSerializer):
    answers = serializers.ListField(required=False)

    class Meta:
        model = Response
        fields = ['questionnaire_id', 'temp_data', 'is_completed', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])
        response = Response.objects.create(**validated_data)
        
        if answers_data:
            for answer_data in answers_data:
                Answer.objects.create(
                    response_id=response,
                    question_id_id=answer_data['question_id'],
                    value=answer_data['value']
                )
        
        return response

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers', None)
        instance = super().update(instance, validated_data)
        
        if answers_data is not None:
            # 先删除旧的答案
            instance.answer_set.all().delete()
            # 创建新的答案
            for answer_data in answers_data:
                Answer.objects.create(
                    response_id=instance,
                    question_id_id=answer_data['question_id'],
                    value=answer_data['value']
                )
        
        return instance
