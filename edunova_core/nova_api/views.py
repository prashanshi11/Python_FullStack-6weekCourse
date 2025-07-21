from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from course_galaxy.models import Course
from quizverse.models import Quiz, Question, Choice, QuizResult

from .serializers import (
    CourseSerializer,
    QuizSerializer,
    QuizDetailSerializer,
    QuizSubmissionSerializer
)

# List all courses
class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# List all quizzes
class QuizListAPIView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

# Quiz detail (with questions & choices)
class QuizDetailAPIView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    lookup_field = 'id'

# Submit a quiz and calculate score
class QuizSubmissionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuizSubmissionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.save()
            # Handle both single and multiple results
            if isinstance(result, list):
                total_score = sum(r.score for r in result)
                total_questions = sum(r.quiz.questions.count() for r in result)
            else:
                total_score = result.score
                total_questions = result.quiz.questions.count()
            return Response({
                "message": "Quiz submitted successfully.",
                "score": total_score,
                "total": total_questions
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
