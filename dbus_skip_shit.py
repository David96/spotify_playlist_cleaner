#!/usr/bin/env python

import dbus

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(redirect_uri='http://localhost:8080',
    scope='user-modify-playback-state,user-read-currently-playing'))

DBusGMainLoop(set_as_default=True)
loop = GLib.MainLoop()

artists = {}
current_track = ''

def handler(interface, changed_props, inv_props):
    global current_track
    if current_track != changed_props['Metadata']['mpris:trackid']:
        current_track = changed_props['Metadata']['mpris:trackid']
        track = sp.track(current_track)
        track_artists = track['artists']
        for artist in track_artists:
            if artist['id'] not in artists:
                artists[artist['id']] = sp.artist(artist['id'])
            a = artists[artist['id']]
            print(a['name'])
            if 'schlager' in a['genres']:
                print('Schlager detected! Skipping…')
                print(track['name'])
                sp.next_track()

bus = dbus.SessionBus()
proxy = bus.get_object('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
interface = dbus.Interface(proxy, dbus_interface='org.freedesktop.DBus.Properties')
interface.connect_to_signal('PropertiesChanged', handler)
loop.run()
