"""
"""
import collections as collections
import logging as logging
import json as json

from dataclasses import dataclass


def get_song_uploads(ytmusic):
    logging.basicConfig( level=logging.INFO)
    return SongUploads(ytmusic)


class SongUploads:
    """Retrieves songs from YouTube Music uploads
    """
    def __init__(self, ytmusic):
        self._ytmusic = ytmusic
        self._songs = None
        
    def get_songs(self):
        logging.info('Retrieving uploads...')
        self._songs = self._ytm_lookup_songs() if not self._songs else self._songs
        return self._songs
    
    def songs_by_year(self):
        songs = self.get_songs()
        songs_by_year = collections.OrderedDict()
        for song in songs:
            year = song.year or 'unknown'
            songs_by_year.setdefault(year, []).append(song)
        return songs_by_year
    
    def read_songs_info(self, reader=None):
        data = reader.read()
        self._songs = [SongInfo(**song) for song in data.get('songs')]
        return self._songs
    
    def write_songs_info(self, file_name, writer=None, lookup_year=False):
        writer = writer or _Writer()
        songs = self.get_songs()
        if lookup_year: self._add_year_to(songs)
        serialized = [song.to_json() for song in songs]
        writer.write(file_name, {'songs': serialized})
        return songs
    
    def _ytm_lookup_songs(self):
        upload_data = self._ytmusic.get_library_upload_songs(limit=None)
        songs = [self._create_song(upload) for upload in upload_data]
        logging.info(f'Found {len(songs)} uploads')
        return songs
    
    def _create_song(self, upload):
        title = upload.get('title')
        artists_info = upload.get('artists', [])
        artist = artists_info[0].get('name') if artists_info else ''
        album_info = upload.get('album', {})
        album = album_info.get('name') if album_info else ''
        return SongInfo(title, artist, album)
    
    def _add_year_to(self, songs):
        for song in songs:
            song.lookup_year(self._ytmusic)


@dataclass
class SongInfo:   
    name: str
    artist: str
    album: str
    year: str
    
    def __init__(self, name, artist, album, year=None):
        self.name = name
        self.artist = artist
        self.album = album
        self.year = year
        
    def lookup_year(self, test_client=None):
        client = test_client or ytmusic
        results = client.search(f"{self.artist} {self.album}", 'albums', limit=1)
        self._add_year(results)
        if self.year: return self.year
        logging.warning(f'No results for {self.name} {self.artist} {self.album}')
        return None
        
    def to_json(self):
        return {
            'name': self.name,
            'artist': self.artist,
            'album': self.album,
            'year': self.year
        }

    def _add_year(self, results):
        for result in results:
            if result.get('resultType') == 'album':
                self.year = result.get('year')
                logging.info(f'Found year {self.year} for {self.name} {self.artist} {self.album}')
                if self.year: return

    def __str__(self):
        return f"{self.name} by {self.artist} on {self.album} ({self.year})"
    
    
class _Reader:
    def read(self, file):
        with self._open(file) as f:
            return self._json_load(f)
        
    def _open(self, file):
        return open(file)
    
    def _json_load(self, file):
        return json.load(file)
    
    
class _Writer:
    def write(self, file, data):
        with self._open(file, mode='w') as f:
            self._json_dump(data, f, indent=4)
            
    def _open(self, file, mode='w'):
        return open(file, mode)
    
    def _json_dump(self, data, file, indent=None):
        json.dump(data, file, indent=indent)