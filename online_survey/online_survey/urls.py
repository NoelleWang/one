from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from online_survey.views import login_view, register_view, dashboard_view

urlpatterns = [
    path('', login_view, name='home'),  # 根路径重定向到登录页面
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('admin/dashboard/', dashboard_view, name='admin_dashboard'),
    path('creator/dashboard/', dashboard_view, name='creator_dashboard'),
    path('analyst/dashboard/', dashboard_view, name='analyst_dashboard'),
    path('respondent/dashboard/', dashboard_view, name='respondent_dashboard'),
    path('api/', include('users.urls')),
    path('api/', include('questionnaires.urls')),
    path('api/', include('answers.urls')),
    path('api/', include('analyses.urls')),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
