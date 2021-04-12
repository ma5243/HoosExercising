from django.test import TestCase
from django.urls import reverse

from oauth.models import Profile
from oauth.tests import create_user
# Create your tests here.

class ExerciseModelTests(TestCase):
    # Test to make sure that the user's points increase when a new exercise is added
    def test_points_earned(self):
        new_user = create_user(username="pointsincrease")
        new_user.save()

        initial_points = new_user.profile.points

        self.client.force_login(new_user)
        self.client.post(reverse('submit_exercise'), {
            'type': 'Strength', 
            'name': 'Squats',
            'tags': ('Legs', 'Calves', 'Core')
        })

        updated_profile = Profile.objects.get(pk=new_user.profile)


        self.assertGreater(updated_profile.points, initial_points)
