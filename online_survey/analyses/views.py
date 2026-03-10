from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from analyses.models import AnalysisTask, Violation
from analyses.serializers import AnalysisTaskSerializer, AnalysisTaskCreateSerializer, ViolationSerializer, ViolationCreateSerializer
from answers.models import Response, Answer
from questionnaires.models import Questionnaire
from django.utils import timezone
import pandas as pd
import os
import tempfile

class AnalysisTaskViewSet(viewsets.ModelViewSet):
    queryset = AnalysisTask.objects.all()
    serializer_class = AnalysisTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create']:
            return AnalysisTaskCreateSerializer
        return AnalysisTaskSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return AnalysisTask.objects.all()
        elif user.role == 'analyst':
            return AnalysisTask.objects.filter(analyst_id=user)
        elif user.role == 'creator':
            return AnalysisTask.objects.filter(questionnaire_id__creator_id=user)
        return AnalysisTask.objects.none()

    def create(self, request):
        user = request.user
        if user.role not in ['admin', 'analyst']:
            return Response({'error': 'Only admin and analyst can create analysis tasks'}, status=status.HTTP_403_FORBIDDEN)

        serializer = AnalysisTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save(analyst_id=user, status='pending')
            # 异步处理分析任务
            self.process_analysis_task(task)
            return Response(AnalysisTaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_analysis_task(self, task):
        try:
            task.status = 'processing'
            task.save()

            questionnaire = task.questionnaire_id
            responses = Response.objects.filter(questionnaire_id=questionnaire, is_completed=1)

            # 准备数据
            data = []
            questions = questionnaire.question_set.all().order_by('order')
            question_ids = [q.id for q in questions]
            question_texts = [q.content for q in questions]

            for response in responses:
                row = {'response_id': response.id, 'created_at': response.created_at}
                for question_id, question_text in zip(question_ids, question_texts):
                    answer = Answer.objects.filter(response_id=response, question_id=question_id).first()
                    if answer:
                        if isinstance(answer.value, list):
                            row[question_text] = ','.join(map(str, answer.value))
                        else:
                            row[question_text] = answer.value
                    else:
                        row[question_text] = ''
                data.append(row)

            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix=f'.{task.export_format.lower()}', delete=False) as tmp:
                if task.export_format == 'Excel':
                    df = pd.DataFrame(data)
                    df.to_excel(tmp.name, index=False)
                elif task.export_format == 'SPSS':
                    # 这里简化处理，实际需要使用pyreadstat库生成sav文件
                    df = pd.DataFrame(data)
                    df.to_csv(tmp.name, index=False)

                # 保存结果路径
                task.result_url = tmp.name
                task.status = 'completed'
                task.save()
        except Exception as e:
            task.status = 'failed'
            task.save()
            print(f"Error processing analysis task: {e}")

class ViolationViewSet(viewsets.ModelViewSet):
    queryset = Violation.objects.all()
    serializer_class = ViolationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create']:
            return ViolationCreateSerializer
        return ViolationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Violation.objects.all()
        return Violation.objects.none()

    def create(self, request):
        user = request.user
        if user.role != 'admin':
            return Response({'error': 'Only admin can create violation records'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ViolationCreateSerializer(data=request.data)
        if serializer.is_valid():
            violation = serializer.save()
            return Response(ViolationSerializer(violation).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        user = request.user
        if user.role != 'admin':
            return Response({'error': 'Only admin can update violation records'}, status=status.HTTP_403_FORBIDDEN)

        violation = self.get_object()
        serializer = ViolationSerializer(violation, data=request.data)
        if serializer.is_valid():
            violation = serializer.save(processed_by=user, processed_at=timezone.now())
            return Response(ViolationSerializer(violation).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
