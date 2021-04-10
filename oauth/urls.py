from django.urls import path

from . import views

urlpatterns = [
    path('', views.self_profile, name='profile'),
    path('<int:profile_id>/', views.specific_profile, name='specific_profile'),
    path('edit/', views.edit_or_redirect, name='edit_profile'),
]
