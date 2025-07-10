from django.shortcuts import render,redirect
from .models import Person
from .forms import PersonForm
# Create your views here.

def person_list(request):
    people = Person.objects.all()
    return render(request,"data/person_list.html",{'people':people})

def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm()
    return render(request, 'data/add_person.html', {'form': form})
