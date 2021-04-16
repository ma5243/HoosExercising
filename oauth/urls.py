from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.self_profile, name='profile'),
    path('profile/<int:profile_id>/', views.specific_profile, name='specific_profile'),
    path('profile/edit/', views.edit_or_redirect, name='edit_profile'),
]
