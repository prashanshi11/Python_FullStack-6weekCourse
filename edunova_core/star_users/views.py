from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Determine group name
            group_name = 'Instructor' if form.cleaned_data.get('is_instructor') else 'Student'
            
            # Get or create group safely
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'star_users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    
    return render(request, 'star_users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    return render(request, 'star_users/home.html', {'user': request.user})


def about_view(request):
    return render(request, 'star_users/about.html')