import random
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Question, Answer


@login_required
def my_history(request):
    answers = (Answer.objects
               .filter(user=request.user)
               .select_related("question")[:100])   # 直近100件
    return render(request, "exams/my_history.html", {"answers": answers})



# ---------- ① トップページ ----------
def home(request):
    years = (Question.objects
             .values_list("exam_year", flat=True)
             .distinct()
             .order_by("-exam_year"))

    nums = [5, 10, 15, 20]          # ← ここで用意して渡す

    return render(request, "exams/home.html", {
        "years": years,
        "nums":  nums,
    })


# ---------- ② 演習スタート ----------
def start_quiz(request):
    """
    POST: 年度・科目・出題数を受け取ってセッション初期化
    """
    if request.method != "POST":
        return redirect("home")

    year  = request.POST["year"]           # 例: "R06"
    part  = request.POST.get("part", "A")  # 今回は A 固定でも OK
    total = int(request.POST.get("num", 20))

    request.session["solved_questions"] = []
    request.session["results"] = []
    request.session["cat"]    = f"FE_{year}{part}"
    request.session["total"]  = total
    request.session.modified  = True
    return redirect("take_quiz")


# ---------- ③ 問題を出す ----------
def take_quiz(request):
    # 進捗
    solved = request.session.get("solved_questions", [])
    total  = request.session.get("total", 0)
    cat    = request.session.get("cat", "")

    # POST（回答が返ってきた）
    if request.method == "POST":
        qid   = int(request.POST["qid"])
        guess = request.POST.get("choice") or ""
        q     = Question.objects.get(id=qid)

        # --- 未選択なら同じ問題を再表示 -----------------
        if not guess:
            choices = [
                ("a", q.choice_a), ("b", q.choice_b),
                ("c", q.choice_c), ("d", q.choice_d),
            ]
            messages.error(request, "選択肢を選んでください。")
            return render(
                request,
                "exams/quiz.html",
                {
                    "question": q,
                    "choices":  choices,
                    "current":  len(request.session.get("solved_questions", [])) + 1,
                    "total":    request.session.get("total", 0),
                },
            )

        # --- 回答がある場合だけここに来る ---------------
        is_ok = (guess == q.correct)

        # ログインしていれば履歴保存
        if request.user.is_authenticated:
            Answer.objects.create(
                user       = request.user,
                question   = q,
                is_correct = is_ok,
                guess      = guess,
            )

        # セッション更新
        sess = request.session
        sess.setdefault("solved_questions", []).append(qid)
        sess.setdefault("results", []).append(is_ok)
        sess.setdefault("guesses", {})[str(qid)] = guess
        sess.modified = True



    
    # 未出題を絞り込む
    unsolved = (Question.objects
                .filter(category=cat)
                .exclude(id__in=solved)
                [: max(total - len(solved), 0)])

    # 全問終わった？
    if not unsolved.exists() or len(solved) >= total:
        return redirect("show_result")

    # 次の1問をランダムで
    q = random.choice(list(unsolved))
    choices = [
        ("a", q.choice_a), ("b", q.choice_b),
        ("c", q.choice_c), ("d", q.choice_d),
    ]
    context = {
        "question": q,
        "choices": choices,
        "current": len(solved) + 1,
        "total": total,
    }


    return render(request, "exams/quiz.html", context)


# ---------- ④ 結果 ----------
def show_result(request):
    ids      = request.session.get("solved_questions", [])
    results  = request.session.get("results", [])      # True / False
    guesses  = request.session.get("guesses", {})      # qid → a/b/c/d

    question_results = []
    for qid, ok in zip(ids, results):
        q = Question.objects.get(id=qid)
        question_results.append({
            "text":    q.text,
            "correct": q.correct,
            "guess":   guesses.get(str(qid), ""),
            "is_ok":   ok,
        })

    context = {
        "correct_count": sum(results),
        "total":         len(results),
        "question_results": question_results,
    }
    return render(request, "exams/show_result.html", context)


# ---------- ⑤ セッションリセット ----------
def reset_session(request):
    request.session.flush()
    return redirect("home")

# ----------⑥ユーザー登録---------
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)          # 作ったら即ログイン
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "exams/signup.html", {"form": form})


