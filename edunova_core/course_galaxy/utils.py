# course_galaxy/utils.py (create this file)
from django.contrib.auth.decorators import user_passes_test

def instructor_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.is_instructor
    )(view_func)
    return decorated_view_func
