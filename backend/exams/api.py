from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id", "text",
            "choice_a","choice_b","choice_c","choice_d",
            "correct", "exam_year", "exam_part",
        ]

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/questions/
    GET /api/questions/?exam_year=R06&exam_part=A&limit=5
    """
    serializer_class = QuestionSerializer

    def get_queryset(self):
        qs = Question.objects.all()
        # 1) フィルタ
        year = self.request.query_params.get("exam_year")
        part = self.request.query_params.get("exam_part")
        if year:
            qs = qs.filter(exam_year=year)
        if part:
            qs = qs.filter(exam_part=part)
        # 2) ランダム n 件
        limit = self.request.query_params.get("limit")
        if limit:
            qs = qs.order_by("?")[: int(limit)]
        return qs

@api_view(["GET"])
def year_list(request):
    """
    GET /api/years/ → ["R06","R05",...]
    """
    years = (
        Question.objects
        .values_list("exam_year", flat=True)
        .distinct()
        .order_by("-exam_year")
    )
    return Response(list(years))
