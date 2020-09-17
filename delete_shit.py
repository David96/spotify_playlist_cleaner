#!/usr/bin/env python

import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri='http://localhost:8080',
    scope='playlist-modify-private'))

if len(sys.argv) != 2:
    print('Usage: ./delete_shit.py playlist_id')
    sys.exit(-1)

playlist_id = sys.argv[1]
wendler_id = '3nrxbDUVMUDDrBCRposrDL'

offset = 0
artists = {}
while True:
    response = sp.playlist_items("spotify:playlist:%s"%playlist_id,
                                 offset=offset,
                                 additional_types=['track'])
    if len(response['items']) == 0:
        break
    for item in response['items']:
        for artist in item['track']['artists']:
            if artist['id'] == wendler_id:
                print('Wendler detected!')
                print(item['track']['name'])
                sp.playlist_remove_all_occurrences_of_items(playlist_id, [item['track']['id']])
                continue
            if artist['id'] not in artists:
                artists[artist['id']] = sp.artist(artist['id'])
            a = artists[artist['id']]
            if 'schlager' in a['genres']:
                print('Up for review: %s' % item['track']['name'])
    offset = offset + len(response['items'])
    print(offset, "/", response['total'])
