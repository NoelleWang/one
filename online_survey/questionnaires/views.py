from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from questionnaires.models import Template, Questionnaire, Question
from questionnaires.serializers import TemplateSerializer, QuestionnaireSerializer, QuestionnaireCreateSerializer, QuestionSerializer
from django.utils import timezone

class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Template.objects.all()
        return Template.objects.all()  # 所有用户都可以查看模板

    def create(self, request):
        user = request.user
        if user.role != 'admin':
            return Response({'error': 'Only admin can create templates'}, status=status.HTTP_403_FORBIDDEN)
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return QuestionnaireCreateSerializer
        return QuestionnaireSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Questionnaire.objects.all()
        elif user.role == 'creator':
            return Questionnaire.objects.filter(creator_id=user)
        return Questionnaire.objects.none()

    def create(self, request):
        user = request.user
        if user.role not in ['admin', 'creator']:
            return Response({'error': 'Only admin and creator can create questionnaires'}, status=status.HTTP_403_FORBIDDEN)
        serializer = QuestionnaireCreateSerializer(data=request.data)
        if serializer.is_valid():
            questionnaire = serializer.save(creator_id=user)
            return Response(QuestionnaireSerializer(questionnaire).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        user = request.user
        questionnaire = self.get_object()
        if user.role != 'admin' and questionnaire.creator_id != user:
            return Response({'error': 'You can only update your own questionnaires'}, status=status.HTTP_403_FORBIDDEN)
        serializer = QuestionnaireCreateSerializer(questionnaire, data=request.data)
        if serializer.is_valid():
            questionnaire = serializer.save()
            return Response(QuestionnaireSerializer(questionnaire).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = request.user
        questionnaire = self.get_object()
        if user.role != 'admin' and questionnaire.creator_id != user:
            return Response({'error': 'You can only delete your own questionnaires'}, status=status.HTTP_403_FORBIDDEN)
        questionnaire.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Question.objects.all()
        elif user.role == 'creator':
            return Question.objects.filter(questionnaire_id__creator_id=user)
        return Question.objects.none()
