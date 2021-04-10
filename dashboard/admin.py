from django.contrib import admin

from .models import Exercise

# Register your models here.

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    fields =('entry_date', 'time', 'journal', 'points_earned', 'owner', 'name', 'type', 'parts_worked')