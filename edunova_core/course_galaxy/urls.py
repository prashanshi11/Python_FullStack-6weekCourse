from django.urls import path
from . import views

urlpatterns = [
    # Instructor URLs
    path('instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('instructor/add-course/', views.add_course, name='add_course'),
    path('instructor/<int:course_id>/add-lesson/', views.add_lesson, name='add_lesson'),

    # Student URLs
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('<int:course_id>/enroll/', views.enroll_in_course, name='enroll_in_course'),

    # Course & Lesson Views
    path('all/', views.course_list, name='course_list'),
    path('lesson/<int:lesson_id>/complete/', views.complete_lesson, name='complete_lesson'),
    path('certificate/<int:course_id>/', views.generate_certificate, name='generate_certificate'),

    # Homepage & Course Details
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
]
