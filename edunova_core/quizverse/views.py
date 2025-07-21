from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice, QuizResult
from .forms import QuizForm, QuestionForm, ChoiceFormSet
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import openpyxl
from django.utils.timezone import localtime

# ✅ List all quizzes
def quiz_list_view(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizverse/quiz_list.html', {'quizzes': quizzes})

# ✅ Take a specific quiz
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz).prefetch_related('choices')

    if request.method == 'POST':
        score = 0
        for q in questions:
            selected = request.POST.get(str(q.pk))
            correct = Choice.objects.filter(question=q, is_correct=True).first()
            if selected and correct is not None and selected == str(correct.pk):
                score += 1
        QuizResult.objects.create(user=request.user, quiz=quiz, score=score)
        return render(request, 'quizverse/result.html', {
            'score': score,
            'total': questions.count()
        })

    return render(request, 'quizverse/take_quiz.html', {
        'quiz': quiz,
        'questions': questions
    })

# ✅ Quiz History for the logged-in user
@login_required
def quiz_history_view(request):
    results = QuizResult.objects.filter(user=request.user).select_related('quiz').order_by('-taken_at')
    return render(request, 'quizverse/history.html', {'results': results})

# ✅ Leaderboard for a specific quiz
def leaderboard_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    top_scores = QuizResult.objects.filter(quiz=quiz).select_related('user').order_by('-score', '-taken_at')[:10]
    return render(request, 'quizverse/leaderboard.html', {'quiz': quiz, 'top_scores': top_scores})

# ✅ Instructor Dashboard
@login_required
def instructor_dashboard(request):
    quizzes = Quiz.objects.filter(instructor=request.user)
    return render(request, 'quizverse/instructor/dashboard.html', {'quizzes': quizzes})

# ✅ Create a new quiz
@login_required
def create_quiz_view(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.instructor = request.user
            quiz.save()
            return redirect('add_question', quiz.id)
    else:
        form = QuizForm()
    return render(request, 'quizverse/instructor/create_quiz.html', {'form': form})

# ✅ Add question and choices to a quiz
@login_required
def add_question_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, instructor=request.user)

    if request.method == 'POST':
        q_form = QuestionForm(request.POST)
        c_formset = ChoiceFormSet(request.POST)

        if q_form.is_valid() and c_formset.is_valid():
            question = q_form.save(commit=False)
            question.quiz = quiz
            question.save()
            choices = c_formset.save(commit=False)
            for choice in choices:
                choice.question = question
                choice.save()
            return redirect('add_question', quiz_id=quiz.pk)
    else:
        q_form = QuestionForm()
        c_formset = ChoiceFormSet()

    return render(request, 'quizverse/instructor/add_question.html', {
        'quiz': quiz,
        'q_form': q_form,
        'c_formset': c_formset
    })

# ✅ Export PDF
@login_required
def export_quiz_results_pdf(request, quiz_id):
    from io import BytesIO
    quiz = get_object_or_404(Quiz, id=quiz_id, instructor=request.user)
    results = QuizResult.objects.filter(quiz=quiz).select_related('user').order_by('-score')

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 14)
    p.drawString(100, 800, f"Quiz Results for: {quiz.title}")

    y = 760
    question_count = Question.objects.filter(quiz=quiz).count()
    for result in results:
        p.drawString(100, y, f"{result.user.username} - {result.score}/{question_count} - {result.taken_at.strftime('%Y-%m-%d %H:%M')}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{quiz.title}_results.pdf"'
    return response

# ✅ Export Excel
@login_required
def export_quiz_results_excel(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, instructor=request.user)
    results = QuizResult.objects.filter(quiz=quiz).select_related('user')

    wb = openpyxl.Workbook()
    ws = wb.active
    if ws is not None:
        ws.title = "Results"

    ws.append(["Username", "Score", "Date Taken"])

    for result in results:
        ws.append([result.user.username, result.score, localtime(result.taken_at).strftime('%Y-%m-%d %H:%M')])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{quiz.title}_results.xlsx"'
    wb.save(response)
    return response

# ✅ Edit Quiz
@login_required
def edit_quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, instructor=request.user)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('instructor_dashboard')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quizverse/instructor/edit_quiz.html', {'form': form, 'quiz': quiz})

# ✅ Delete Quiz
@login_required
def delete_quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, instructor=request.user)
    if request.method == 'POST':
        quiz.delete()
        return redirect('instructor_dashboard')
    return render(request, 'quizverse/instructor/confirm_delete.html', {'quiz': quiz})
