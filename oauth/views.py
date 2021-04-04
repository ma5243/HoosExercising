from django.shortcuts import render

# Create your views here.

class SignupView(allauth.account.views.SignupView):
    template_name = 'signup.html'
    pass