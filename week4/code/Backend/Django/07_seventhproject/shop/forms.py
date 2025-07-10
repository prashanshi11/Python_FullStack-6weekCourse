from django import forms
from .models import Product, ProductDetail

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'detail', 'tags']

class ProductDetailForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = ['description', 'warranty']
