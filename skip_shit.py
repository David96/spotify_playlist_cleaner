#!/usr/bin/env python

import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri='http://localhost:8080',
    scope='user-modify-playback-state,user-read-currently-playing'))

artists = {}
while True:
    current_track = sp.currently_playing()['item']
    print('Playing: %s' % current_track['name'])
    for artist in current_track['artists']:
        if artist['id'] not in artists:
            artists[artist['id']] = sp.artist(artist['id'])
        a = artists[artist['id']]
        if 'schlager' in a['genres']:
            print('Schlager detected! Skipping…')
            print(current_track['name'])
            sp.next_track()

    time.sleep(5)
