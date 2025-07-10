from django.contrib import admin
from .models import Category, Tag, ProductDetail, Product

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ProductDetail)
admin.site.register(Product)
