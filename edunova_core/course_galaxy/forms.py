from django import forms
from .models import Course, Lesson, Review

# 📘 Course Creation Form
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'thumbnail', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter course description...'}),
            'title': forms.TextInput(attrs={'placeholder': 'Course Title'}),
        }

# 🎥 Lesson Creation Form
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_url']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Lesson content or notes...'}),
            'video_url': forms.URLInput(attrs={'placeholder': 'https://youtube.com/...'}),
        }

# ⭐ Course Review Form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your review...',
                'class': 'review-content-box',
            }),
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'review-rating-input',
            }),
        }
