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

####################################
#  EXTRA CODE, MAY BE USED LATER
#  client_id = '686f63c1a0564bfda4f0c9165efa21ef'
#  client_secret = '2477e715839840b4b6e42749d22bbbdc'
#  redirect_uri = 'http://127.0.0.1:8000/music/playlist/'
#  scope = "playlist-modify-public"
#  sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
#  playlists = sp.user_playlists('spotify')
#  return HttpResponse(playlists)
#def playlist2(request):
#    client_id = '686f63c1a0564bfda4f0c9165efa21ef'
#    client_secret = '2477e715839840b4b6e42749d22bbbdc'
#    template = loader.get_template('spotify/index.html')
#    sp = obtain_spotify_object(client_id, client_secret)
#    top_hits = retrieve_top_hits(sp)
#    song1 = retrieve_song(sp, "Levitating", "Dua Lipa")
#    song2 = retrieve_song(sp, "Body", "Megan Thee Stallion")
#    song3 = retrieve_song(sp, "Juicy", "Doja Cat")
#    song4 = retrieve_song(sp, "Motivation", "Normani")
#    song5 = retrieve_song(sp, "Wake Me Up", "Avici")
#    songs = [song1, song2, song3, song4, song5]
#
#    context = {
#        'top': top_hits,
#        'music': songs,
#    }
#    return HttpResponse(template.render(context, request))
#
# def extra_code(request):
#    client_id = '686f63c1a0564bfda4f0c9165efa21ef'
#    client_secret = '2477e715839840b4b6e42749d22bbbdc'
#    redirect_uri = 'http://127.0.0.1:8000/music/'
#    scope = "playlist-modify-public"
#    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
#    user_ID = sp.current_user()['id']
#    song_url = request.POST.get('song')
#    sp.user_playlist_create(sp.current_user()["id"], "Hoos Exercising Jams", public=True, collaborative=False, description='Music for your workout, provided by Hoos Exercisin')
#    return HttpResponse(sp.artist('spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'))
#    return index(request)
#    sp.current_user_saved_tracks_add(tracks=[song_url])
#    return index(request)
#
#    initial_search = sp_caller.search(q='track:' + str(song_title) + " artist:" + str(artist_name), type='track')
#    recommended_song = initial_search['tracks']['items'][0]
#    recommended_song_title = recommended_song['name']
#    recommended_song_image = recommended_song['album']['images'][0]['url']
#    recommended_song_link = recommended_song['external_urls']['spotify']
#    return {
#        'title': recommended_song_title,
#        'artist': artist_name,
#        'image': recommended_song_image,
#        'link': recommended_song_link
#    }
################################

###########
# SOURCES: https://www.programiz.com/python-programming/list
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