from django.urls import path
from . import views

urlpatterns = [
    path("quiz/", views.take_quiz, name="take_quiz"),
]

