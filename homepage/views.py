from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime

# Create your views here.

#@login_required
def index(request):
    template = loader.get_template('homepage/index.html')
    context = {
        
    }
    return HttpResponse(template.render(context, request))
    #return HttpResponse("Hey I'm just testing this!")