# exams/serializers.py
from rest_framework import serializers
from .models import Question, Answer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Question
        fields = [
            "id", "text",
            "choice_a", "choice_b", "choice_c", "choice_d",
            "correct", "exam_year", "exam_part",
        ]

class AnswerSerializer(serializers.ModelSerializer):
    # question.text と question.correct を読み取り専用で追加
    question_text  = serializers.CharField(source="question.text", read_only=True)
    correct_answer = serializers.CharField(source="question.correct", read_only=True)
    # guess → user_answer にエイリアス
    user_answer    = serializers.CharField(source="guess")

    class Meta:
        model  = Answer
        fields = [
            "id",
            "question_text",
            "user_answer",
            "correct_answer",
            "is_correct",
        ]