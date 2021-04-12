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

    def test_retrieve_song_correct_title(self):
        obj = views.obtain_spotify_object(self.client_id, self.client_secret)
        song_title = "Juicy"
        song_artist = "Doja Cat"
        test_song = views.retrieve_song(obj, song_title, song_artist)
        self.assertEqual(test_song['title'], song_title)  

    def test_retrieve_song_correct_artist(self):
        obj = views.obtain_spotify_object(self.client_id, self.client_secret)
        song_title = "Juicy"
        song_artist = "Doja Cat"
        test_song = views.retrieve_song(obj, song_title, song_artist)
        self.assertEqual(test_song['artist'], song_artist) 

###############################
# SOURCE: https://intellipaat.com/community/9924/call-a-function-from-another-file-in-python#:~:text=If%20you%20want%20to%20call,b)and%20you%20are%20done.
###############################