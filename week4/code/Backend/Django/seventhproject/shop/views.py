# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm, ProductDetailForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        detail_form = ProductDetailForm(request.POST)
        product_form = ProductForm(request.POST)
        if detail_form.is_valid() and product_form.is_valid():
            detail = detail_form.save()
            product = product_form.save(commit=False)
            product.detail = detail
            product.save()
            product_form.save_m2m()
            return redirect('product_list')
    else:
        detail_form = ProductDetailForm()
        product_form = ProductForm()
    return render(request, 'shop/add_product.html', {
        'product_form': product_form,
        'detail_form': detail_form
    })

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')
