from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Profile

class DummyTest(TestCase):
    def test_dummy(self):
        self.assertIs(True, True)

class ProfileCreationTest(TestCase):
    # Create a new user and make sure that an associated profile is created as well.
    def test_create_profile(self):
        User = get_user_model()
        new_user = User.objects.create(username="tester", first_name="John", last_name="Doe", email="jd@example.com")
        self.assertIsInstance(new_user.profile, Profile)
        new_user.save()