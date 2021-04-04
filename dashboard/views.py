from django.shortcuts import render
from .models import Exercise
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.

def index(request):
    template = loader.get_template('dashboard/index.html')
    user_exercises = Exercise.objects.filter(owner__exact=13)

    context = {
        'user_exercises': user_exercises,
    }
    return HttpResponse(template.render(context, request))

@login_required
def submit_exercise(request):
    e_type = request.POST['type']
    e_name = request.POST['name']
    e_tags = request.POST['tags'].split(',')
    e = Exercise(owner=request.user.id, type=e_type, name=e_name, parts_worked=e_tags)
    e.save()
    return HttpResponseRedirect('/dashboard')