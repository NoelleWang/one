from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from answers.models import Response, Answer
from answers.serializers import ResponseSerializer, ResponseCreateSerializer
from questionnaires.models import Questionnaire
from django.utils import timezone

class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'admin':
                return Response.objects.all()
            elif user.role == 'creator':
                return Response.objects.filter(questionnaire_id__creator_id=user)
            elif user.role == 'analyst':
                return Response.objects.all()
            elif user.role == 'respondent':
                return Response.objects.filter(respondent_id=user)
        return Response.objects.none()

    def create(self, request):
        questionnaire_id = request.data.get('questionnaire_id')
        try:
            questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        except Questionnaire.DoesNotExist:
            return Response({'error': 'Questionnaire not found'}, status=status.HTTP_404_NOT_FOUND)

        # 检查问卷状态
        if questionnaire.status != 'published':
            return Response({'error': 'Questionnaire is not published'}, status=status.HTTP_403_FORBIDDEN)

        # 检查问卷有效期
        now = timezone.now()
        if questionnaire.start_time and now < questionnaire.start_time:
            return Response({'error': 'Questionnaire has not started yet'}, status=status.HTTP_403_FORBIDDEN)
        if questionnaire.end_time and now > questionnaire.end_time:
            return Response({'error': 'Questionnaire has expired'}, status=status.HTTP_403_FORBIDDEN)

        # 检查IP限制
        ip_address = request.META.get('REMOTE_ADDR')
        if questionnaire.ip_limit:
            existing_response = Response.objects.filter(
                questionnaire_id=questionnaire,
                ip_address=ip_address,
                is_completed=1
            ).exists()
            if existing_response:
                return Response({'error': 'You have already completed this questionnaire from this IP'}, status=status.HTTP_403_FORBIDDEN)

        # 检查最大填写次数
        if questionnaire.max_responses > 0:
            completed_responses = Response.objects.filter(
                questionnaire_id=questionnaire,
                is_completed=1
            ).count()
            if completed_responses >= questionnaire.max_responses:
                return Response({'error': 'Questionnaire has reached maximum responses'}, status=status.HTTP_403_FORBIDDEN)

        # 创建填写记录
        respondent = request.user if request.user.is_authenticated else None
        response_data = {
            'questionnaire_id': questionnaire,
            'respondent_id': respondent,
            'ip_address': ip_address,
            'temp_data': request.data.get('temp_data'),
            'is_completed': request.data.get('is_completed', 0)
        }

        serializer = ResponseCreateSerializer(data=response_data)
        if serializer.is_valid():
            response = serializer.save()
            return Response(ResponseSerializer(response).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        response = self.get_object()
        questionnaire = response.questionnaire_id

        # 检查问卷状态
        if questionnaire.status != 'published':
            return Response({'error': 'Questionnaire is not published'}, status=status.HTTP_403_FORBIDDEN)

        # 检查问卷有效期
        now = timezone.now()
        if questionnaire.end_time and now > questionnaire.end_time:
            return Response({'error': 'Questionnaire has expired'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ResponseCreateSerializer(response, data=request.data)
        if serializer.is_valid():
            response = serializer.save()
            return Response(ResponseSerializer(response).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def check_eligibility(self, request):
        questionnaire_id = request.query_params.get('questionnaire_id')
        try:
            questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        except Questionnaire.DoesNotExist:
            return Response({'error': 'Questionnaire not found'}, status=status.HTTP_404_NOT_FOUND)

        # 检查问卷状态
        if questionnaire.status != 'published':
            return Response({'eligible': False, 'message': 'Questionnaire is not published'})

        # 检查问卷有效期
        now = timezone.now()
        if questionnaire.start_time and now < questionnaire.start_time:
            return Response({'eligible': False, 'message': 'Questionnaire has not started yet'})
        if questionnaire.end_time and now > questionnaire.end_time:
            return Response({'eligible': False, 'message': 'Questionnaire has expired'})

        # 检查IP限制
        ip_address = request.META.get('REMOTE_ADDR')
        if questionnaire.ip_limit:
            existing_response = Response.objects.filter(
                questionnaire_id=questionnaire,
                ip_address=ip_address,
                is_completed=1
            ).exists()
            if existing_response:
                return Response({'eligible': False, 'message': 'You have already completed this questionnaire from this IP'})

        # 检查最大填写次数
        if questionnaire.max_responses > 0:
            completed_responses = Response.objects.filter(
                questionnaire_id=questionnaire,
                is_completed=1
            ).count()
            if completed_responses >= questionnaire.max_responses:
                return Response({'eligible': False, 'message': 'Questionnaire has reached maximum responses'})

        return Response({'eligible': True, 'message': 'You are eligible to fill this questionnaire'})
