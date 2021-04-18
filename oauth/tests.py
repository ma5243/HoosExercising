from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Profile

class ProfileModelTest(TestCase):
    # Test the height stringification on a normal case
    def test_height_normal(self):
        prof = create_user().profile
        prof.height = 74 # 6 ft 2 inches
        self.assertTupleEqual((6, 2), prof.readable_height)
    def test_height_negative(self):
        prof = create_user().profile
        prof.height = -12
        self.assertTupleEqual((0, 0), prof.readable_height)
    def test_height_boundary(self):
        prof = create_user().profile
        prof.height = 72
        self.assertTupleEqual((6, 0), prof.readable_height)
    def test_height_boundary2(self):
        prof = create_user().profile
        prof.height = 71
        self.assertTupleEqual((5, 11), prof.readable_height)

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

class ProfilePageTest(TestCase):
    # Basic test, ensure that user's characteristics and the edit profile button shows up on their own profile page.
    def test_new_profile(self):
        new_user = create_user(first_name = 'new_prof_test')
        new_user.profile.weight = 1234
        new_user.profile.points = 9999
        new_user.profile.bio = "unit test bio"
        new_user.profile.save()
        
        self.client.force_login(new_user)
        response = self.client.get(reverse('profile'))
        self.assertContains(response, '1234')
        self.assertContains(response, 9999)
        self.assertContains(response, 'unit test bio')
        self.assertContains(response, 'Edit')

    # Test to ensure that updating the profile with a POST actually changes the profile page.
    def test_profile_change(self):
        new_user = create_user(first_name = 'update_test')
        new_user.profile.weight = 74
        new_user.profile.bio = "I should be changed"
        new_user.profile.save()
        self.client.force_login(new_user)
        self.client.post(reverse('edit_profile'), {
            'bio': 'New bio',
            'height': 72,
            'weight': 75,
            'points': 0,
        })
        response = self.client.get(reverse('profile'))
        self.assertNotContains(response,'I should be changed')
        self.assertNotContains(response, '6 ft 2 in')
        self.assertContains(response, 'New bio')


    def test_nonexistent_profile_id(self):
        response = self.client.get(reverse('profile') + '/999')
        self.assertEqual(response.status_code, 404)
    

class FriendsTest(TestCase):
    # Test that users can friend one another
    def test_friend_basic(self):
        friender = create_user(username="friender")
        friend_target = create_user(username="friendtarget")

        self.client.force_login(friender)
        self.client.post(reverse('add_friend'),{
            'new_friend_pk': friend_target.profile.pk
        })
        self.assertIn(friend_target.profile, friender.profile.friends.all())
    # Test that friends can be removed
    def test_friend_remove(self):
        friender = create_user(username="friender")
        friend_target = create_user(username="friendtarget")

        self.client.force_login(friender)
        self.client.post(reverse('add_friend'),{
            'new_friend_pk': friend_target.profile.pk
        })
        self.client.post(reverse('remove_friend'), {
            'remove_friend_pk': friend_target.profile.pk
        })
        self.assertNotIn(friend_target.profile, friender.profile.friends.all())