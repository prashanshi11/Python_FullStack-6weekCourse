from django.shortcuts import render

def data_views(request):
    return render(request, 'data/index.html')  # assuming this is your template
