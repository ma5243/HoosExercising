from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def obtain_spotify_object(client_id, client_secret):
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

def retrieve_song(sp_caller, song_title, artist_name):
    initial_search = sp_caller.search(q='track:' + str(song_title) + " artist:" + str(artist_name), type='track')
    recommended_song = initial_search['tracks']['items'][0]
    recommended_song_title = recommended_song['name']
    recommended_song_image = recommended_song['album']['images'][0]['url']
    recommended_song_link = recommended_song['external_urls']['spotify']
    return {
        'title': recommended_song_title,
        'artist': artist_name,
        'image': recommended_song_image,
        'link': recommended_song_link
    }

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

def index(request):
    client_id = '686f63c1a0564bfda4f0c9165efa21ef'
    client_secret = '2477e715839840b4b6e42749d22bbbdc'
    template = loader.get_template('spotify/index.html')
    sp = obtain_spotify_object(client_id, client_secret)
    top_hits = retrieve_top_hits(sp)
    song1 = retrieve_song(sp, "Levitating", "Dua Lipa")
    song2 = retrieve_song(sp, "Body", "Megan Thee Stallion")
    song3 = retrieve_song(sp, "Juicy", "Doja Cat")
    song4 = retrieve_song(sp, "Motivation", "Normani")
    song5 = retrieve_song(sp, "Wake Me Up", "Avici")
    songs = [song1, song2, song3, song4, song5]

    context = {
        'top': top_hits,
        'music': songs,
    }
    return HttpResponse(template.render(context, request))

###########
# SOURCES: https://www.programiz.com/python-programming/list
#          https://developer.spotify.com/documentation/web-api/
#          https://developer.spotify.com/documentation/web-api/reference/
#          https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
#          https://www.youtube.com/watch?v=xdq6Gz33khQ
#          https://github.com/codingforentrepreneurs/30-Days-of-Python/tree/master/tutorial-reference/Day%2019/notebooks
#          https://github.com/plamere/spotipy/issues/83
#          https://spotipy.readthedocs.io/en/2.17.1/
#          https://stackoverflow.com/questions/56791883/typeerror-can-only-concatenate-str-not-set-to-str
###########