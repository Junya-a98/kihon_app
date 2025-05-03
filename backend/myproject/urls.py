# myproject/urls.py

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView
from accounts.views import MeAPIView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from exams.api import (
    QuestionViewSet,
    year_list,
    #AnswerViewSet,
)
router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
#router.register(r'answers',   AnswerViewSet,   basename='answer')  # optional

urlpatterns = [
    # React ルート（index.html）を返す
    path('', TemplateView.as_view(template_name="index.html")),

    # 管理画面、認証
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # JWT 認証エンドポイント
    path('api/token/',         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),    name='token_refresh'),

    # DRF ViewSet 一式
    path('api/', include(router.urls)),

    # カスタムで「年度一覧だけ返す」APIが必要なら別パスに
    path('api/years/', year_list, name='year-list'),

    path("api/users/me/", MeAPIView.as_view(), name="users-me"),
]
