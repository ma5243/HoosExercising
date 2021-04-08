from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Exercise(models.Model):
    entry_date = models.DateTimeField(verbose_name="Date and Time of Workout")
    time = models.PositiveSmallIntegerField(verbose_name="Length of Workout (in minutes)", null=True)
    journal = models.CharField(verbose_name="Post-Workout Thoughts", max_length=200, null=True)
    points_earned = models.PositiveIntegerField(verbose_name="Points from Workout", default=5)
    owner = models.IntegerField()
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    parts_worked = ArrayField(models.CharField(max_length=50), blank=True)