from django.shortcuts import render, get_object_or_404
from .models import Student

def home(request):
    students = Student.objects.all()
    return render(request, 'students/home.html', {'students': students})

def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'students/detail.html', {'student': student})
