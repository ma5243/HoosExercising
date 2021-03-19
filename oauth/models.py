from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Wrap the User object within a Profile, gives name and email.
    signup_date = models.DateField(verbose_name="User signup date")

    bio = models.CharField(verbose_name="User Bio", max_length=200)
    height = models.PositiveSmallIntegerField(verbose_name="Height in inches", blank=True) # Doesn't allow for fractional height, integers only
    weight = models.PositiveSmallIntegerField(verbose_name="Weight in pounds", blank=True) 

    points = models.PositiveIntegerField(verbose_name="Total accumulated points")


    def __str__(self):
        return self.user.first_name + self.user.last_name + ": " + self.points
