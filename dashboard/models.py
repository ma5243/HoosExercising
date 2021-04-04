from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Exercise(models.Model):
    owner = models.IntegerField()
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    parts_worked = ArrayField(models.CharField(max_length=50), blank=True)