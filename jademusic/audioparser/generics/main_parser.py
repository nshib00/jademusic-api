from rest_framework.request import Request

from audioparser.hitmo.parser import (
    parse_hitmo,
    parse_tracks_to_download as download_hitmo_tracks,
    parse_tracks_to_get as get_hitmo_tracks,
    parse_playlists_to_download as download_hitmo_playlists,
    parse_playlists_to_get as get_hitmo_playlists,
    parse_albums_to_download as download_hitmo_albums,
    parse_albums_to_get as get_hitmo_albums,
)
# from audioparser.mp3party.parser import (
#     parse_albums_to_download as download_mp3party_albums,
#     parse_mp3party,
#     parse_albums_to_get as get_mp3party_albums
# )

def start_track_parser(request: Request, action='download') -> None:
    match action:
        case 'download':
            parse_hitmo(request, parser=download_hitmo_tracks)
        case 'get':
            parse_hitmo(request, parser=get_hitmo_tracks)


def start_album_parser(request: Request, action='download') -> None:
    match action:
        case 'download':
            parse_hitmo(request, parser=download_hitmo_albums)
        case 'get':
            parse_hitmo(request, parser=get_hitmo_albums)


def start_playlist_parser(request: Request, action='download') -> None:
    match action:
        case 'download':
            parse_hitmo(request, parser=download_hitmo_playlists)
        case 'get':
            parse_hitmo(request, parser=get_hitmo_playlists)
