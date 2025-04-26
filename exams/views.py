import random
from django.shortcuts import render, redirect
from .models import Question

def take_quiz(request):
    """
    GET  : ランダムに 1 問出題
    POST : 回答を採点して結果画面へ
    """
    if request.method == "POST":
        qid   = int(request.POST["qid"])
        guess = request.POST.get("choice")  # '' の可能性もある
        q     = Question.objects.get(id=qid)
        result = (guess == q.correct)
        context = {
            "question": q,
            "guess": guess,
            "result": result,
        }
        return render(request, "exams/result.html", context)

    # --- GET ---
    q = random.choice(Question.objects.all())
    choices = [
        ('a', q.choice_a),
        ('b', q.choice_b),
        ('c', q.choice_c),
        ('d', q.choice_d),
    ]
    return render(request, "exams/quiz.html", {"question": q, "choices": choices})
