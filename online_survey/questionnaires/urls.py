from django.urls import path, include
from rest_framework.routers import DefaultRouter
from questionnaires.views import TemplateViewSet, QuestionnaireViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'templates', TemplateViewSet)
router.register(r'questionnaires', QuestionnaireViewSet)
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
