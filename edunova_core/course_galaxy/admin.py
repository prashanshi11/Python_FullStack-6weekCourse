from django.contrib import admin
from .models import Course, Lesson, Category

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lesson)
