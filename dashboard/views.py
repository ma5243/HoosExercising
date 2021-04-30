from django.shortcuts import render
from .models import Exercise
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime


# Create your views here.

@login_required
def index(request):
    template = loader.get_template('dashboard/index.html')
    user_exercises = Exercise.objects.filter(owner__exact=request.user.id)
    context = {
        'user_exercises': user_exercises,
    }
    return HttpResponse(template.render(context, request))

@login_required
def submit_exercise(request):
    e_type = request.POST['type']
    e_name = request.POST['name']
    e_tags = request.POST['tags'].split(',')
    e = Exercise(owner=request.user.id, type=e_type.capitalize(), name=e_name.capitalize(), parts_worked=[ t.capitalize() for t in e_tags ], entry_date=datetime.now())
    e.save()
    return HttpResponseRedirect('/dashboard')

@login_required
def get_exercise(request):
    e_id = request.POST.get('id', -1)
    exercise = Exercise.objects.filter(owner__exact=request.user.id).filter(id__exact=e_id)
    if(len(exercise) == 0):
        raise Http404
    else:
        return JsonResponse(exercise.values()[0])

@login_required
def delete_exercise(request):
    e_id = request.POST.get('id', -1)
    exercise = Exercise.objects.filter(owner__exact=request.user.id).filter(id__exact=e_id)
    print(e_id)
    if(len(exercise) == 0):
        raise Http404
    else:
        exercise[0].delete()
        return HttpResponse(status=200)

@login_required
def set_journal(request):
    e_id = request.POST.get('id', -1)
    e_journal_contents = request.POST['journal_contents']
    exercise = Exercise.objects.filter(owner__exact=request.user.id).filter(id__exact=e_id)
    if(len(exercise) == 0):
        raise Http404
    else:
        exercise[0].journal = e_journal_contents
        exercise[0].save()
        return HttpResponse(status=200)