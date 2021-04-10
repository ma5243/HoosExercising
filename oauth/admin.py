from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ('user','points','signup_date', 'bio', 'profile_photo')