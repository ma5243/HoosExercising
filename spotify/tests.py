from django.test import TestCase

from . import views

# Create your tests here.

class SpotifyTests(TestCase):
    client_id = '686f63c1a0564bfda4f0c9165efa21ef'
    client_secret = '2477e715839840b4b6e42749d22bbbdc'

    def test_obtain_spotify_object(self):
        # Test that we obtain a non-null Spotipy object
        obj = views.obtain_spotify_object(self.client_id, self.client_secret)
        self.assertIsNotNone(obj)

    def test_retrieve_top_hits(self):
        # Test that Spotify retrieves the correct playlist
        obj = views.obtain_spotify_object(self.client_id, self.client_secret)
        top_hits = views.retrieve_top_hits(obj)
        self.assertEqual(top_hits['title'], "Today's Top Hits")  

    def test_select5_not_null(self):
        # Test that the function to obtain five songs retrieves a list of songs
        obj = views.obtain_spotify_object(self.client_id, self.client_secret)
        top_hits_link = views.retrieve_top_hits(obj)['link']
        test_songs = views.select5(obj, top_hits_link)
        self.assertIsNotNone(test_songs)

    def test_select5_correct_length(self):
        # Test that the function to obtain five songs retrieves 5 songs exactly
        obj = views.obtain_spotify_object(self.client_id, self.client_secret)
        top_hits_link = views.retrieve_top_hits(obj)['link']
        test_songs = views.select5(obj, top_hits_link)
        sample_size = [1, 2, 3, 4, 5]
        self.assertEquals(len(test_songs), 5)

###############################
# SOURCE: https://intellipaat.com/community/9924/call-a-function-from-another-file-in-python#:~:text=If%20you%20want%20to%20call,b)and%20you%20are%20done.
###############################