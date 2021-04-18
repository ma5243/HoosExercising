from django.urls import path

from . import views

urlpatterns = [
    path('', views.self_profile, name='profile'),
    path('<int:profile_id>/', views.specific_profile, name='specific_profile'),
    path('edit/', views.edit_or_redirect, name='edit_profile'),
    path('friends/', views.friend_list, name='friend_list'),
    path('friends/add', views.add_friend, name='add_friend'),
    path('friends/remove', views.remove_friend, name='remove_friend'),
]
