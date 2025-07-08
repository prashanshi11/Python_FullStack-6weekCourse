from django.http import HttpResponse

def members(request):
    return HttpResponse("This is the members page of the Django project.")