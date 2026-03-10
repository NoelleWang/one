from django.urls import path, include
from rest_framework.routers import DefaultRouter
from analyses.views import AnalysisTaskViewSet, ViolationViewSet

router = DefaultRouter()
router.register(r'analysis-tasks', AnalysisTaskViewSet)
router.register(r'violations', ViolationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
