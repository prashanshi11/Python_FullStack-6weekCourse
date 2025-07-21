from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    CourseListAPIView,
    QuizListAPIView,
    QuizDetailAPIView,
    QuizSubmissionAPIView,
)

router = DefaultRouter()

urlpatterns = [
    path('courses-list/', CourseListAPIView.as_view(), name='api_course_list'),
    path('quizzes-list/', QuizListAPIView.as_view(), name='api_quiz_list'),
    path('quizzes-detail/<int:id>/', QuizDetailAPIView.as_view(), name='api_quiz_detail'),
    path('submit-quiz/', QuizSubmissionAPIView.as_view(), name='api_submit_quiz'),
    path('get-token/', obtain_auth_token, name='api_token_auth'),
    path('', include(router.urls)),  # Optional if you add ViewSets later
]
