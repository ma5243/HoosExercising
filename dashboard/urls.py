from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit_exercise', views.submit_exercise, name='submit_exercise')
]