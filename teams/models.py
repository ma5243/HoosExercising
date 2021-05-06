from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

#model for actual team structure. includes team name and list of team members.
class Team(models.Model):
    name = models.CharField(max_length = 75)
    team_description = models.TextField(max_length = 1000)
    team_members = models.ManyToManyField(User, symmetrical=True, verbose_name="Team Members", null=True)

    def __str__(self):
        return self.name

#posts to the team page.
class Posts(models.Model):
    title = models.CharField(max_length = 50)
    post_body = models.TextField(max_length = 1000)

    def __str__(self):
        return self.title

    