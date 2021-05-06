from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

import spotipy
import random
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# Retrieves Spotify object to make function calls to Spotify API
def obtain_spotify_object(client_id, client_secret):
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Retrieves information on a song from the Top Hits Playlist
def retrieve_song(index, top_hits_songs):
    recommended_song = top_hits_songs[index]['track']
    recommended_song_primary_artist = recommended_song['artists'][0]['name']
    recommended_song_title = recommended_song['name']
    recommended_song_image = recommended_song['album']['images'][0]['url']
    recommended_song_link = recommended_song['external_urls']['spotify']
    return {
        'title': recommended_song_title,
        'artist': recommended_song_primary_artist,
        'image': recommended_song_image,
        'link': recommended_song_link
    }

# Retrieves Spotify's "Today's Top Hits" playlist
def retrieve_top_hits(sp_caller):
    general_playlists = sp_caller.user_playlists('spotify')
    top_hits = general_playlists['items'][0]
    name = top_hits['name']
    link = top_hits['external_urls']['spotify']
    image = top_hits['images'][0]['url']
    return {
        'title': name,
        'image': image,
        'link': link
    }

# Obtains 5 random songs from the "Today's Top Hits" playlist for users to view
def select5(sp_caller, top_hits_link):
    top_hits_songs = sp_caller.playlist_tracks(playlist_id=top_hits_link, limit=100)['items']
    five_songs = random.sample(range(0, 50), 5)
    song_data = []
    for i in five_songs:
        song = retrieve_song(i, top_hits_songs)
        song_data.append(song)
    return song_data

# An intermediary webpage used in order for the refresh button to obtain new songs for the user
def songs(request):
    return index(request)

# Obtains the Top Hits playlist and 5 songs from the playlist for the user
def index(request):
    client_id = '686f63c1a0564bfda4f0c9165efa21ef'
    client_secret = '2477e715839840b4b6e42749d22bbbdc'
    template = loader.get_template('spotify/index.html')
    sp = obtain_spotify_object(client_id, client_secret)
    top_hits = retrieve_top_hits(sp)
    top_hits_link = top_hits['link']
    songs = select5(sp, top_hits_link)
    context = {
        'top': top_hits,
        'music': songs,
    }
    return HttpResponse(template.render(context, request))

###########
# SOURCES FOR WORKING WITH PYTHON AND THE SPOTIPY API:
#          https://www.programiz.com/python-programming/list
#          https://developer.spotify.com/documentation/web-api/
#          https://developer.spotify.com/documentation/web-api/reference/
#          https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
#          https://www.youtube.com/watch?v=xdq6Gz33khQ
#          https://github.com/codingforentrepreneurs/30-Days-of-Python/tree/master/tutorial-reference/Day%2019/notebooks
#          https://github.com/plamere/spotipy/issues/83
#          https://spotipy.readthedocs.io/en/2.17.1/
#          https://spotipy.readthedocs.io/en/2.18.0
#          https://stackoverflow.com/questions/56791883/typeerror-can-only-concatenate-str-not-set-to-str
#          https://spotipy.readthedocs.io/en/2.18.0/
#          https://stackoverflow.com/questions/58473385/how-to-access-radio-button-selected-value-in-django
#          https://www.geeksforgeeks.org/iterate-over-a-list-in-python/
#          https://www.journaldev.com/33182/python-add-to-list
#          https://stackoverflow.com/questions/22842289/generate-n-unique-random-numbers-within-a-range
#          
###########

#/***************************************************************************************
#  SPOTIFY API REFERENCE
#  Title: Welcome to Spotipy!
#  Author: Paul Lamere
#  Date: 2014
#  Code version: 2.18.0
#  URL: https://github.com/plamere/spotipy
#  Software License: MIT License
#***************************************************************************************/