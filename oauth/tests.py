from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Profile

class ProfileCreationTest(TestCase):
    # Create a new user and make sure that an associated profile is created as well.
    def test_create_profile(self):
        new_user = create_user(first_name='creator')
        self.assertIsInstance(new_user.profile, Profile)
        new_user.save()


def create_user(username="Tester", first_name="John", last_name="Doe", email="jd@example.com"):
    User = get_user_model()
    new_user = User.objects.create(username = username, first_name = first_name, last_name = last_name, email = email)
    return new_user

class ProfileUpdateTest(TestCase):
    # Basic test, ensure that user's characteristics and the edit profile button shows up on their own profile page.
    def test_new_profile(self):
        new_user = create_user(first_name = 'new_prof_test')
        new_user.profile.weight = 1234
        new_user.profile.bio = "unit test bio"
        new_user.profile.save()
        
        self.client.force_login(new_user)
        response = self.client.get(reverse('profile'))
        self.assertContains(response, '1234')
        self.assertContains(response, 'unit test bio')
        self.assertContains(response, 'Update Profile')

    # Test to ensure that updating the profile with a POST actually changes the profile page.
    def test_profile_change(self):
        new_user = create_user(first_name = 'update_test')
        new_user.profile.weight = 555
        new_user.profile.bio = "I should be changed"
        new_user.profile.save()
        self.client.force_login(new_user)
        self.client.post(reverse('edit_profile'), {
            'bio': 'New bio',
            'height': 123,
            'weight': 75,
            'points': 0
        })
        response = self.client.get(reverse('profile'))
        self.assertNotContains(response,'I should be changed')
        self.assertNotContains(response, '555')
        self.assertContains(response, 'New bio')
        self.assertContains(response, '123')



    # Make sure that trying to update the profile with an invalid PK returns a 404