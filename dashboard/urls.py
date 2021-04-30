from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit_exercise', views.submit_exercise, name='submit_exercise'),
    path('get_exercise', views.get_exercise, name='get_exercise'),
    path('set_journal', views.set_journal, name='set_journal'),
    path('delete_exercise', views.delete_exercise, name='delete_exercise')
]