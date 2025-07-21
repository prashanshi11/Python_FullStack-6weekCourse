from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_instructor = forms.BooleanField(required=False, label="Register as Instructor")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'bio', 'profile_pic', 'is_instructor']
