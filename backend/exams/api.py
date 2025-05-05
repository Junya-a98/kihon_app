from rest_framework import serializers, viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Answer,Question
from .serializers import AnswerSerializer

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
    queryset = Question.objects.all() 

    def get_queryset(self):
        qs = Question.objects.all()

        # --- フィルタ ---
        year = self.request.query_params.get("exam_year")
        part = self.request.query_params.get("exam_part")
        if year and year.lower() != "null":
            qs = qs.filter(exam_year=year)
        if part and part.lower() != "null":
            qs = qs.filter(exam_part=part)

        # --- ランダム n 件 ---
        raw_limit = self.request.query_params.get("limit")
        try:
            limit = int(raw_limit) if raw_limit and raw_limit.lower() != "null" else None
        except ValueError:
            limit = None   # 数字でなければ無視

        if limit:
            qs = qs.order_by("?")[:limit]

        return qs

class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class   = AnswerSerializer
    queryset = Question.objects.all() 

    def get_queryset(self):
        return Answer.objects.filter(user=self.request.user)

class SubmitAnswerAPIView(APIView):
    """
    POST /api/submit_answer/
    {
      "question_id": 12,
      "user_answer": "b"
    }
    """
    authentication_classes = [JWTAuthentication]   # ← これを追加
    permission_classes     = [IsAuthenticated]     # ログイン済みなら誰でも OK

    def post(self, request):

        q_id = request.data.get("question_id")
        user_ans = request.data.get("user_answer")
        q = Question.objects.get(id=q_id)

        if not q_id or user_ans not in ("a","b","c","d"):
            return Response({"detail":"bad payload"}, status=400)

        
        Answer.objects.create(
            user=request.user,
            question=q,
            guess=user_ans,
            is_correct=(user_ans == q.correct)
        )
        return Response(status=status.HTTP_201_CREATED)

class AnswerSummaryAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]

    def get(self, request):
        # 直近5回分をセッションごとにまとめて返すイメージ
        qs = (
            Answer.objects
            .filter(user=request.user)
            .order_by('-solved_at')
        )
        # ここでは 1 問 = 1 レコード想定。answered_at を 1 回のクイズ単位で group by など
        summary = []
        for a in qs:
            summary.append({
                "solved_at": a.solved_at,
                "correct":   1 if a.is_correct else 0,
                "total":     1,
            })
        return Response(summary[:5])  # 直近5件

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
