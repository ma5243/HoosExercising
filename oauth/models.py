import os

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings

from django.dispatch import receiver
from django.db.models.signals import post_save



class Profile(models.Model):
    # Wrap the User object within a Profile, gives name and email.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE,primary_key=True)
    signup_date = models.DateField(verbose_name="User signup date")

    profile_photo = models.ImageField(verbose_name="Profile picure", upload_to='profile_photos/', null=True) 
    bio = models.CharField(verbose_name="User Bio", max_length=200, null=True)
    height = models.PositiveSmallIntegerField(verbose_name="Height in inches", null=True) # Doesn't allow for fractional height, integers only
    weight = models.PositiveSmallIntegerField(verbose_name="Weight in pounds", null=True) 

    points = models.PositiveIntegerField(verbose_name="Total accumulated points", default=0)

    #friends = models.ManyToManyField("self", symmetrical=True, verbose_name="Friend list", null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + "(" + str(self.pk) + "): " + str(self.points) + " accumulated points"

    # Get the profile photo path for the user 
    # Returns just a placeholder if not set, otherwise returns the actual photo
    # The heroku filesystem is ephemerakl, so photos get deleted over time.
    def photo_or_placeholder(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url
        return settings.STATIC_URL + 'profile_placeholder.jpg'

    # Get the human-readable height for a user.
    # Returns a tuple of (feet, inches) which is (0,0) on invalid input
    @property
    def readable_height(self):
        # Integer divide by 12 to get feet, remainder is inches
        if not self.height or self.height <= 0:
            return (0,0)
        ft = self.height // 12
        inches = self.height % 12
        return (ft, inches)

    class Meta:
        ordering = ['-points']

# Allauth fires a post_save signal when a new user signs up.
# We can catch this signal and create a sensible default profile and initialize the one-to-one relationship.
@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_profile(sender, created, instance, **kwargs):
    # The signal fires multiple times, so we need to make sure that this one is the actual creator of the user profile.
    if created:
        new_profile = Profile(user = instance, bio="Placeholder bio", signup_date=timezone.now())
        new_profile.save()

### NOT CURRENTLY BEING USED (REFER INSTEAD TO dashboard/models.py) - DO NOT DELETE, CONTAINS USEFUL CODE ###
#class Exercise(models.Model):
#    # Create an Exercise model that can store the basic information about exercises that a user would complete
#    # Each Profile would then have an associated list of exercise objects, each instance referring to the date the exercise was recorded
#    # Workout dropdown categories for the type of exercise, body part exercised, and workout intensity conducted
#    TYPES_OF_EXERCISE = (
#        (1, _('Balance')),
#        (2, _('Cardio')),
#        (3, _('Flexibility')),
#        (4, _('Strength')),
#        (5, _('Other')),
#    )
#    TYPES_OF_BODY_PARTS = (
#        (1, _('Abdominals')),
#        (2, _('Arms')),
#        (3, _('Back')),
#        (4, _('Chest')),
#        (5, _('Legs')),
#        (6, _('Shoulders')),
#        (7, _('Other')),
#    )
#    INTENSITY = (
#        (1, _('Low')),
#        (2, _('Moderate')),
#        (3, _('Vigorous')),
#    )
#    # Exercise fields
#    entry_date = models.DateTimeField(verbose_name="Date and Time of Workout")
#    exercise_type = models.CharField(max_length=15, choices=TYPES_OF_EXERCISE, default=1,)
#    body_part_exercised = models.CharField(max_length=15, choices=TYPES_OF_BODY_PARTS, default=1,)
#    exercise_intensity = models.CharField(max_length=15, choices=INTENSITY, default=1,)
#    time = models.PositiveSmallIntegerField(verbose_name="Length of Workout (in minutes)", null=True)
#    journal = models.CharField(verbose_name="Post-Workout Thoughts", max_length=200, null=True)
#    points_earned = models.PositiveIntegerField(verbose_name="Points from Workout", default=5)
#
#    def __str__(self):
#        return "Earned " + str(self.points_earned) + " with a workout on " + self.entry_date + ", focused on " + self.body_part_exercised + " with " + self.exercise_type + " exercises for " + str(self.time) + " minutes"



#####################################
# RUNNING LIST OF SOURCES
# Source for Exercise Model: https://www.merixstudio.com/blog/django-models-declaring-list-available-choices-right-way/
# Source for Types of Exercise: https://www.bupa.co.uk/health-information/exercise-fitness/types-of-exercise
# Muscle Group Workout Information: https://www.medicalnewstoday.com/articles/muscle-groups-to-work-out-together#which-muscle-groups-to-pair
# DateTime Field: https://www.geeksforgeeks.org/datetimefield-django-models/
# Intensity Scale: https://en.wikipedia.org/wiki/Exercise_intensity
# Model Format: https://docs.djangoproject.com/en/3.1/intro/tutorial02/
######################################
