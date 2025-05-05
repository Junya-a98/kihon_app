# backend/myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import MeAPIView, RegisterAPIView
from exams.api import (
    QuestionViewSet,
    AnswerViewSet,
    SubmitAnswerAPIView,
    AnswerSummaryAPIView,
    year_list,
)

router = DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"answers",   AnswerViewSet,   basename="answer")

urlpatterns = [
    # ========= API =========
    path("api/token/",         TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(),    name="token_refresh"),

    path("api/users/me/",      MeAPIView.as_view(),           name="users-me"),
    path("api/register/",      RegisterAPIView.as_view(),     name="users-register"),

    path("api/years/",         year_list,                     name="year-list"),
    path("api/submit_answer/", SubmitAnswerAPIView.as_view()),
    path("api/answers/summary/", AnswerSummaryAPIView.as_view()),  # ★ ここが router より前

    # ViewSet 一式（最後にまとめて）
    path("api/", include(router.urls)),

    # ========= Django 標準 =========
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),

    # ========= React SPA =========
    path("", TemplateView.as_view(template_name="index.html")),
]
