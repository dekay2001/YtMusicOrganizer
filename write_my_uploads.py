import os

import ytmusicapi as ytmusic

import ytm.organizer as organizer

from ytmusicapi import YTMusic
ytmusic = YTMusic("oauth.json")

SONGS_FILE = os.path.join(os.getcwd(), 'my-songs-with-yearbolt.json')

song_uploads = organizer.get_song_uploads(ytmusic)
song_uploads.write_songs_info(SONGS_FILE, lookup_year=True)