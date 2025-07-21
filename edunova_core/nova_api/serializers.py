from rest_framework import serializers
from course_galaxy.models import Course
from quizverse.models import Quiz, Question, Choice, QuizResult

# Course serializer
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

# Quiz serializer (basic info)
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

# Nested serializers for questions and choices
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']

class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'questions']

# Serializer for submitting a quiz
class QuizSubmissionSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    answers = serializers.DictField(child=serializers.IntegerField())  # {question_id: choice_id}

    def validate(self, data):
        quiz_id = data['quiz_id']
        answers = data['answers']
        for qid in answers.keys():
            if not Question.objects.filter(id=qid, quiz_id=quiz_id).exists():
                raise serializers.ValidationError(f"Invalid question ID {qid} for quiz {quiz_id}")
        return data

    def create(self, validated_data):
        quiz = Quiz.objects.get(id=validated_data['quiz_id'])
        user = self.context['request'].user
        answers = validated_data['answers']
        score = 0

        for qid, cid in answers.items():
            question = Question.objects.get(id=qid)
            if Choice.objects.filter(id=cid, question=question, is_correct=True).exists():
                score += 1

        result = QuizResult.objects.create(user=user, quiz=quiz, score=score)
        return result
