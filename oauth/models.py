from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    # Wrap the User object within a Profile, gives name and email.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE) 
    signup_date = models.DateField(verbose_name="User signup date")

    bio = models.CharField(verbose_name="User Bio", max_length=200, null=True)
    height = models.PositiveSmallIntegerField(verbose_name="Height in inches", null=True) # Doesn't allow for fractional height, integers only
    weight = models.PositiveSmallIntegerField(verbose_name="Weight in pounds", null=True) 

    points = models.PositiveIntegerField(verbose_name="Total accumulated points", default=0)


    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + ": " + str(self.points) + " accumulated points"

# Allauth fires a post_save signal when a new user signs up.
# We can catch this signal and create a sensible default profile and initialize the one-to-one relationship.
@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_profile(sender, created, instance, **kwargs):
    # The signal fires multiple times, so we need to make sure that this one is the actual creator of the user profile.
    if created:
        new_profile = Profile(user = instance, bio="Placeholder bio", signup_date=timezone.now())
        new_profile.save()