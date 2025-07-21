from django import forms
from .models import Quiz, Question, Choice
from django.forms import modelformset_factory

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'course']  # ✅ Adjust as per your final model

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

# ✅ Define a ChoiceForm
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']

# ✅ Create the formset to handle multiple choices per question
ChoiceFormSet = modelformset_factory(
    Choice,
    form=ChoiceForm,
    extra=4,  # You can change this to how many choices per question you want
    can_delete=False
)
