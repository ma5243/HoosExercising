from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

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
    journal = models.CharField(max_length=2000)

    def __str__(self):
        return "(" + str(self.owner) + "): " + self.type + " - " + self.name 

# We can catch a signal sent by the exercise model to increase the user's points
# Prevents us from having to iterate over all exercises, can instead be constant time.
@receiver(post_save, sender = Exercise)
def update_points(sender, instance, created, **kwargs):
    User = get_user_model()
    profile = User.objects.get(id = instance.owner).profile
    profile.points += (float)(sender.time) / 6 # Hardcoded 5, TODO update dynamically based on intensity/time
    sender.points_earned = (float)(sender.time) / 6
    profile.save()
