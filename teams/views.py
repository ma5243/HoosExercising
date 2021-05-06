from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.http.response import HttpResponseNotFound

# Create your views here.

#this is the section where you actually write what the code will display.

#okay, here is the goal- have a tab titled teams, where people who belong to teams can see what teams 
#they belong to. In each team's home page they have the list of all the team posts that are there.
#i don't care who can post to the team pages it should just be able to happen.

def index(request):
    #template = loader.get_template('teams/index.html')
    HttpResponse("Teams Page temp")
    #TODO: display in order similar to exercise 

#need another view- the individual team view. Displays team name, description, and the posts to the team page
#def team_page(request):
    #template = loader.get_template('teams/team_page.html')
    #context = TODO- should just be the information specific to the team.
    #HttpResponse(context, template)
