from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Q
import datetime

from .models import Course, Lesson, Enrollment, LessonCompletion, Review, Category
from .forms import CourseForm, LessonForm, ReviewForm
from .utils import instructor_required
from xhtml2pdf import pisa

# ------------------------------------
# 📘 COURSE LISTING with SEARCH + FILTERS
# ------------------------------------
def course_list(request):
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    
    courses = Course.objects.all()
    
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(instructor__username__icontains=search_query)
        )

    if category_filter:
        courses = courses.filter(category_id=category_filter)
    
    categories = Category.objects.all()

    return render(request, 'course_galaxy/course_list.html', {
        'courses': courses,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_filter
    })


# ------------------------------------
# 📘 COURSE DETAIL with REVIEWS
# ------------------------------------
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()

    if enrolled and request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = request.user
            review.save()
            messages.success(request, '✅ Review submitted successfully!')
            return redirect('course_detail', course_id=course.pk)
    else:
        form = ReviewForm()

    reviews = Review.objects.filter(course=course).order_by('-created_at')

    return render(request, 'course_galaxy/course_detail.html', {
        'course': course,
        'form': form,
        'reviews': reviews,
        'enrolled': enrolled
    })


# ------------------------------------
# 👨‍🏫 INSTRUCTOR DASHBOARD & COURSE CREATION
# ------------------------------------
@instructor_required
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'course_galaxy/instructor_dashboard.html', {'courses': courses})


@instructor_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('instructor_dashboard')
    else:
        form = CourseForm()
    return render(request, 'course_galaxy/add_course.html', {'form': form})


@instructor_required
def add_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('instructor_dashboard')
    else:
        form = LessonForm()
    return render(request, 'course_galaxy/add_lesson.html', {'form': form, 'course': course})


# ------------------------------------
# 👨‍🎓 STUDENT: ENROLLMENT & DASHBOARD
# ------------------------------------
@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user.is_instructor:
        return redirect('instructor_dashboard')  # Instructors shouldn't enroll

    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('student_dashboard')


@login_required
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'course_galaxy/student_dashboard.html', {
        'enrollments': enrollments
    })


# ------------------------------------
# ✅ MARK LESSON COMPLETE
# ------------------------------------
@login_required
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if not Enrollment.objects.filter(student=request.user, course=lesson.course).exists():
        return redirect('course_list')  # Can't complete if not enrolled

    LessonCompletion.objects.get_or_create(student=request.user, lesson=lesson)
    return redirect('lesson_detail', lesson_id=lesson.pk)


# ------------------------------------
# 🏆 GENERATE CERTIFICATE (PDF)
# ------------------------------------
@login_required
def generate_certificate(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course)
    completed_lessons = LessonCompletion.objects.filter(student=request.user, lesson__in=lessons)

    if completed_lessons.count() != lessons.count():
        return HttpResponse("You must complete all lessons to get the certificate.")

    template_path = 'course_galaxy/certificate_template.html'
    context = {
        'student_name': request.user.get_full_name() or request.user.username,
        'course_title': course.title,
        'date': datetime.datetime.now().strftime("%B %d, %Y")
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{course.title}_certificate.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status, error = pisa.CreatePDF(html, dest=response) # type: ignore
    if error:
        return HttpResponse('💥 Error generating certificate')
    return response


# ------------------------------------
# 🌐 API: COURSE LIST (Authenticated)
# ------------------------------------
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CourseSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_course_list(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)
