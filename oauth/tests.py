from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Profile

class ProfileCreationTest(TestCase):
    # Create a new user and make sure that an associated profile is created as well.
    def test_create_profile(self):
        new_user = create_profile(first_name='creator')
        self.assertIsInstance(new_user.profile, Profile)
        new_user.save()


def create_profile(username="Tester", first_name="John", last_name="Doe", email="jd@example.com"):
    User = get_user_model()
    new_user = User.objects.create(username = username, first_name = first_name, last_name = last_name, email = email)
    return new_user

class ProfileUpdateTest(TestCase):
    # Ensure that we can modify the profile of a user and the changes propagate to profile page. 

    def test_update_profile(self):
        self.assertEquals(True, True)

    # Make sure that trying to update the profile with an invalid PK returns a 404