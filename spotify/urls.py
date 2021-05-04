from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('spotify/', views.index, name='middle'),
    path('songs/', views.songs, name='songs'),
]