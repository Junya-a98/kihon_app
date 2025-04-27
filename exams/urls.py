from django.urls import path
from . import views

urlpatterns = [
    path("quiz/", views.take_quiz, name="take_quiz"),
    path('', views.home, name='home'),
    path("start/", views.start_quiz, name="start"),    # ← 追加：演習開始 POST
    path('result/', views.show_result, name='show_result'),
    path('reset/', views.reset_session, name='reset_session'),



]

