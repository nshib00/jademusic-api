from audioparser.generics.music_objects import Track, Playlist, Album


def make_track_json_response(track_obj: Track) -> dict:
    # Создание словаря с данными о треке, который в дальнейшем будет конвертирован в JSON-словарь.
    track_json = {
        'id': track_obj.id_,
        'data': track_obj.data
    }
    # Замена отдельных ключей для исполнителя и названия трека на общий ключ с полным названием.
    track_json['data']['full_title'] = track_obj.full_title
    track_json['data'].pop('artist')
    track_json['data'].pop('title')

    # track_json['data']['img'] = site_url + track_json['data']['img']

    return track_json


def make_playlist_json_response(playlist_obj: Playlist) -> dict:
    return {
        'id': playlist_obj.id_,
        'title': playlist_obj.title,
        'url': playlist_obj.url
    }


def make_album_json_response(album_obj: Album) -> dict:
    return {
        'id': album_obj.id_,
        'title': album_obj.title,
        'url': album_obj.url
    }


def make_music_objects_list_json_response(musobj_list) -> list[dict]:
    musobj_list_json = []
    for musobj in musobj_list:
        if isinstance(musobj, Track):
            musobj_list_json.append(make_track_json_response(musobj))
        elif isinstance(musobj, Playlist):
            musobj_list_json.append(make_playlist_json_response(musobj))
        elif isinstance(musobj, Album):
            musobj_list_json.append(make_album_json_response(musobj))
        else:
            raise ValueError(f'List contains non-music object {musobj.__str__}.')
    return musobj_list_json


def make_musobj_json_response(musobj: list) -> list[dict]:
    return [make_track_json_response(track) for track in musobj]


