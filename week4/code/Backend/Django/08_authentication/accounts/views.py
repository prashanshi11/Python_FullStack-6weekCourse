from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirm = request.POST['password2']
        if password == confirm:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            else:
                User.objects.create_user(username=username, password=password, email=email)
                messages.success(request, "Registered successfully. Please login.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'accounts/home.html')
