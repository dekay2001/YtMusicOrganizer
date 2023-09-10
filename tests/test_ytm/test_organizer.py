import unittest as unittest

from assertpy import assert_that

import ytm.organizer as organizer


class TestSongUploads(unittest.TestCase):
    def setUp(self):
        self.ytmusic = self
        self.writer = WriterSpy()
        self.uploads = organizer.SongUploads(self.ytmusic)
        
    def test_get_uploads_specifies_no_limit_to_get_all_songs(self):
        songs = self.uploads.get_songs()
        assert_that(self.ytmusic.specified_limit).is_none()
        
    def test_get_uploads_returns_songs(self):
        songs = self.uploads.get_songs()
        assert_that(len(songs)).is_equal_to(1)
        assert_that(songs[0]).is_instance_of(organizer.SongInfo)
        
    def test_write_songs_info(self):
        file_name = 'path-to-songs.json'
        songs = self.uploads.write_songs_info(file_name, writer=self.writer)
        expected = {"songs":[songs[0].to_json()]}
        assert_that(self.writer.file.name).is_equal_to(file_name)
        self.writer.expect_json_dump(expected, self.writer.file, indent=4)
        
    def test_write_songs_info_can_lookup_year(self):
        file_name = 'path-to-songs.json'
        songs = self.uploads.write_songs_info(file_name, writer=self.writer, lookup_year=True)
        assert_that(songs[0].year).is_equal_to('1994')
        self.expect_search('artist album', 'albums', 1)
        
    def get_library_upload_songs(self, limit):
        # doubling youtubemusic
        self.specified_limit = limit
        return [{'title': 'name', 'artists': [{'name': 'artist'}], 'album': {'name': 'album'}}]

    def search(self, query, filter_str, limit):
        self.special_query = query
        self.special_filter = filter_str
        self.special_limit = limit
        return [{'resultType': 'album', 'year': '1994'}]
    
    def expect_search(self, query, filter_str, limit):
        assert_that(self.special_query).is_equal_to(query)
        assert_that(self.special_filter).is_equal_to(filter_str)
        assert_that(self.special_limit).is_equal_to(limit)


class TestSongInfo(unittest.TestCase):
    def setUp(self):
        self.ytmusic_double = self
        self.song = organizer.SongInfo('name', 'artist', 'album')

    def test_properties(self):
        assert_that(self.song.name).is_equal_to('name')
        assert_that(self.song.artist).is_equal_to('artist')
        assert_that(self.song.album).is_equal_to('album')
        assert_that(self.song.year).is_none()
        
    def test_to_json(self):
        assert_that(self.song.to_json()).is_equal_to({
            'name': 'name',
            'artist': 'artist',
            'album': 'album',
            'year': None
        })
        
    def test_lookup_year_populates_year(self):
        result = self.song.lookup_year(test_client=self.ytmusic_double)
        assert_that(result).is_equal_to('1994')
        assert_that(self.song.year).is_equal_to('1994')
        self.expect_search('artist album', 'albums', 1)
        
    def search(self, query, filter_str, limit):
        self.special_query = query
        self.special_filter = filter_str
        self.special_limit = limit
        return [{'resultType': 'album', 'year': '1994'}]
    
    def expect_search(self, query, filter_str, limit):
        assert_that(self.special_query).is_equal_to(query)
        assert_that(self.special_filter).is_equal_to(filter_str)
        assert_that(self.special_limit).is_equal_to(limit)
        
 
class TestWriter(unittest.TestCase):
    def setUp(self):
        self.writer = WriterSpy()
        self.file = 'some-file.json'
        
    def test_write(self):
        self.writer.write(self.file, {'key': 'value'})
        assert_that(self.writer.file.entered).is_true()
        assert_that(self.writer.mode).is_equal_to('w')
        assert_that(self.writer.file.name).is_equal_to(self.file)
        assert_that(self.writer.file.exited).is_true()
        self.writer.expect_json_dump(
            {'key': 'value'}, 
            self.writer.file, 
            indent=4
        )
        
class WriterSpy(organizer._Writer):
    def __init__(self):
        self.data = None
        self.file = None
        
    def _open(self, file, mode=None):
        self.mode = mode
        self.file = FileDouble(file)
        return self.file
    
    def _json_dump(self, data, file, indent=None):
        self.specified_data = data
        self.specified_file = file
        self.specified_indent = indent
        
    def expect_json_dump(self, data, file, indent=None):
        assert_that(self.specified_data).is_equal_to(data)
        assert_that(self.specified_file).is_equal_to(file)
        assert_that(self.specified_indent).is_equal_to(indent)
    
    
class FileDouble:
    def __init__(self, file):
        self.name = file
        self.entered = False
        self.exited = False
        
    def __enter__(self):
        self.entered = True
        return self
    
    def __exit__(self, type, value, traceback):
        self.exited = True
        pass
    
    def write(self, data):
        self.file = data
    
        
if __name__ == '__main__':
    unittest.main()