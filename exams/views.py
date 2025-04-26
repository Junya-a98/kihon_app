import random
from django.shortcuts import render, redirect
from .models import Question

def home(request):
    return render(request, "exams/home.html")

def take_quiz(request):
    """
    GET  : ランダムに未出題の1問を出題
    POST : 回答を記録し、次の問題へ or 結果へ
    """
    if request.method == "POST":
        qid = int(request.POST["qid"])
        guess = request.POST.get("choice")
        q = Question.objects.get(id=qid)
        result = (guess == q.correct)

        # セッションに記録
        if 'solved_questions' not in request.session:
            request.session['solved_questions'] = []
        if 'results' not in request.session:
            request.session['results'] = []

        request.session['solved_questions'].append(qid)
        request.session['results'].append(result)
        request.session.modified = True

    # --- GET ---
    # 出題済みを除く
    solved = request.session.get('solved_questions', [])
    unsolved = Question.objects.exclude(id__in=solved)

    if not unsolved.exists():
        return redirect('show_result')  # 全問終了したら結果ページへ

    q = random.choice(unsolved)
    choices = [
        ('a', q.choice_a),
        ('b', q.choice_b),
        ('c', q.choice_c),
        ('d', q.choice_d),
    ]
    return render(request, "exams/quiz.html", {"question": q, "choices": choices})

def show_result(request):
    results = request.session.get('results', [])
    correct_count = sum(results)
    total = len(results)
    solved_ids = request.session.get('solved_questions', [])
    solved_questions = Question.objects.filter(id__in=solved_ids)

    # 正誤をペアにしてまとめる
    question_results = []
    for q, res in zip(solved_questions, results):
        question_results.append({
            'text': q.text,
            'correct': q.correct,
            'result': res
        })

    context = {
        "correct_count": correct_count,
        "total": total,
        "question_results": question_results,
    }
    return render(request, "exams/show_result.html", context)


def reset_session(request):
    request.session.flush()  # セッション全部リセット
    return redirect('home')  # トップページに戻る

