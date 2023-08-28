from pathlib import Path


class BaseMusicObject:
    ''' Базовый класс для моделей музыкальных объектов (трек, альбом, плейлист или др.)'''

    def __init__(self, id_, title, url, data):
        self.id_ = id_
        self.title = title
        self.url = url
        self.data = data  # общие данные об объекте

    @staticmethod
    def make_title(artist, title):
        return f'{artist} - {title}'

    @staticmethod
    def make_path(folder_path: str, title: str) -> Path:
        return Path(folder_path, title + '.mp3')


class Track(BaseMusicObject):
    GET_AND_DOWNLOAD_METHODS = ('only_one', 'by_numbers', 'first_n', 'all')
    def __init__(self, id_, artist, title, data, url=None, duration=None):
        self.artist = artist
        self.full_title = self.make_title(artist, title)
        self.duration = duration
        super().__init__(id_, title, url, data)
        self.path = None # путь до трека создается при его скачивании

    def validate_url(self):
        pass


class MusobjWithData(BaseMusicObject):
    def __init__(self, id_, title, url, data=None):
        if data is None:
            data = {}
        super().__init__(id_, title, url, data)


class Playlist(MusobjWithData):
    pass


class Album(MusobjWithData):
    pass


def make_track_object(raw_track: dict, track_id: int) -> Track:
    track_obj = Track(id_=track_id,
                artist=raw_track['artist'],
                title=raw_track['title'],
                data=raw_track,
            )
    if raw_track.get('duration'):
        track_obj.duration = raw_track.get('duration')
    if raw_track.get('url'):
        track_obj.url = raw_track.get('url')
    return track_obj


def make_playlist_object(raw_playlist: dict[str], playlist_id: int) -> Playlist:
    return Playlist(
        id_=playlist_id,
        title=raw_playlist['title'],
        url=raw_playlist['url'],
    )


def make_album_object(raw_album: dict[str], album_id: int) -> Album:
    return Album(
        id_=album_id,
        title=raw_album['title'],
        url=raw_album['url'],
    )