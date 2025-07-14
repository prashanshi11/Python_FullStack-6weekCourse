from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'core/home.html')

def catalog(request):
    products = Product.objects.all()
    return render(request, 'core/catalog.html', {'products': products})

@login_required
def add_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('catalog')
    return render(request, 'core/add_product.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request, 
            username=request.POST['username'], 
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'core/register.html', {'form': form})
