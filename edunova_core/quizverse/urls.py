from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list_view, name='quiz_list'),
    path('<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('history/', views.quiz_history_view, name='quiz_history'),
    path('<int:quiz_id>/leaderboard/', views.leaderboard_view, name='quiz_leaderboard'),
    path('quiz/<int:quiz_id>/export/pdf/', views.export_quiz_results_pdf, name='export_pdf'),
    path('quiz/<int:quiz_id>/export/excel/', views.export_quiz_results_excel, name='export_excel'),
    path('instructor/quiz/<int:quiz_id>/edit/', views.edit_quiz_view, name='edit_quiz'),
    path('instructor/quiz/<int:quiz_id>/delete/', views.delete_quiz_view, name='delete_quiz'),

    # Instructor URLs
    path('instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('instructor/create/', views.create_quiz_view, name='create_quiz'),
    path('instructor/<int:quiz_id>/add-question/', views.add_question_view, name='add_question'),

    # ❌ REMOVE or COMMENT the next line
    # path('instructor/<int:question_id>/add-choice/', views.add_choice_view, name='add_choice'),
]
