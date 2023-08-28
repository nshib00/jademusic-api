from requests import Response
from requests_html import HTMLSession, Element
import logging
from rich.console import Console

from rest_framework.request import Request

from audioparser import download, formatters
from audioparser.generics.responses import make_music_objects_list_json_response, make_musobj_json_response
from audioparser.generics.parser import Parser
from audioparser.generics import html as generics_html

from . import data
from ..generics.music_objects import Track, Playlist, Album

from rest_framework.exceptions import ParseError

from ..paths import PathManager

console = Console()
logger = logging.getLogger(__name__)
logging.basicConfig(format=download.log_format, level='INFO')


class HitmoParser(Parser):
    hitmo = data.HitmoData()

    def get_track_attrs_dict(self, raw_track: Element) -> dict:
        data = {
            'artist': raw_track.find(generics_html.TRACK_ARTIST_HTML, first=True).text,
            'title': raw_track.find(generics_html.TRACK_TITLE_HTML, first=True).text,
            'duration': raw_track.find(generics_html.TRACK_DURATION_HTML, first=True).text,
        }
        return data

    @staticmethod
    def get_new_tracks_url(track_widget: Element) -> str:
        new_tracks_ref_html = track_widget.find(generics_html.TRACKS_WIDGET_HTML, first=True)
        return new_tracks_ref_html.attrs.get('href')

    def parse_and_get_tracks(self, response: Response) -> list[dict]:
        tracks_list = []

        tracks_response = response.html
        tracks_items = tracks_response.find(generics_html.TRACK_HTML)
        tracks_urls = self.parse_tracks_urls(tracks_items)

        for track, track_url in zip(tracks_items, tracks_urls):
            track_dict = self.get_track_attrs_dict(track)
            track_dict['url'] = track_url
            tracks_list.append(track_dict)
        return tracks_list

    def get_tracks_list(self, request: Request, query=None, is_popular=False, is_new=False, artist_url=None) -> list[dict]:
        session = HTMLSession()

        if is_popular:
            url = self.hitmo.popular_tracks_url
        elif is_new:
            url = self.hitmo.new_tracks_url
        else:
            page = self.get_page(request)
            if artist_url is not None:
                url = self.hitmo.get_tracks_pagination_url(page=page, artist_url=artist_url)
            else:
                # url = self.hitmo.search_url + query
                url = self.hitmo.get_tracks_pagination_url(page=page) + query

        response = session.get(url)
        tracks_list = self.parse_and_get_tracks(response)

        return tracks_list

    def _make_playlist_url(self, request_playlist_url):
        if request_playlist_url.startswith('https://') or request_playlist_url.startswith('http://'):
            return request_playlist_url
        else:
            return self.hitmo.url + request_playlist_url

    def make_playlists_url(self, request: Request) -> str:
        page = self.get_page(request)
        return self.hitmo.get_playlists_pagination_url(page=page)

    def get_playlists(self, request: Request) -> list[dict]:
        playlists = []
        session = HTMLSession()
        playlists_url = self.make_playlists_url(request)

        playlists_page = self.get_site_response(request, playlists_url, session)
        playlists_html = playlists_page.html.find(generics_html.PLAYLIST_HTML)
        for playlist in playlists_html:
            playlist_title = playlist.find('span.album-title', first=True).text
            playlist_ref = playlist.find('a.album-link', first=True)
            playlists.append(
                {
                    'title': playlist_title,
                    'url': self._make_playlist_url(request_playlist_url=playlist_ref.attrs.get('href'))
                }
            )
        return playlists

    def make_albums_url(self, request: Request) -> str:
        page = self.get_page(request)
        return self.hitmo.get_albums_pagination_url(page=page)

    def get_albums(self, request: Request) -> list[dict]:
        albums = []
        session = HTMLSession()
        albums_url = self.make_albums_url(request)

        albums_page = self.get_site_response(request, albums_url, session)
        albums_html = albums_page.html.find(generics_html.ALBUM_HTML)
        for album in albums_html:
            album_title = album.find('span.album-title', first=True).text
            album_ref = album.find('a', first=True)
            albums.append(
                {
                    'title': album_title,
                    'url': self._make_playlist_url(request_playlist_url=album_ref.attrs.get('href'))
                }
            )
        return albums


def make_tracks_list(request: Request) -> list[dict]:
    hitmo_parser = HitmoParser()

    if request.query_params.get('popular'):
        return hitmo_parser.get_tracks_list(request, is_popular=True)
    if request.query_params.get('new'):
        return hitmo_parser.get_tracks_list(request, is_new=True)
    else:
        query = formatters.format_query(request.query_params.get('q'))
        if query is None:
            raise ParseError('Некорректный запрос: отсутствует обязательный параметр q.')

        if request.query_params.get('artist'):
            query_url = hitmo_parser.hitmo.search_url + query

            artist_page_url = hitmo_parser.get_artist_page_url(
                query_url,
                artist_html=generics_html.ALBUM_HTML,
            )
            if artist_page_url is not None:
                artist_page_url = hitmo_parser.hitmo.url + artist_page_url

            return hitmo_parser.get_tracks_list(request, query=query, artist_url=artist_page_url)

        return hitmo_parser.get_tracks_list(request, query=query)


def parse_tracks_to_get(request: Request, get_to_download=False) -> list[Track] | None:
    ''' При get_to_download=False parse_to_get работает как независимый парсер.
        При get_to_download=True parse_to_get работает как часть парсера parse_to_download. '''
    hitmo_parser = HitmoParser()

    tracks_list = make_tracks_list(request)

    if get_to_download:
        tracks_list = hitmo_parser.get_tracks_to_download_list(tracks_list, request)
    if len(tracks_list) == 0:
        tracklist = []
        console.print(
            '[#ffff00 bold]По вашему запросу ничего не найдено. Проверьте, не ошиблись ли в названии трека/исполнителя и попробуйте еще раз.\n[/]')
    else:
        tracklist = hitmo_parser.get_track_objects_list(tracks_list)
        print('Найдено треков:', len(tracklist))

    request.data['tracks'] = make_music_objects_list_json_response(musobj_list=tracklist)

    if get_to_download:
        hitmo_parser.check_request_folder(request)
        return tracklist


def parse_tracks_to_download(request: Request) -> None:
    tracklist = parse_tracks_to_get(request, get_to_download=True)
    download.download_tracks(folder_path=PathManager.download_path, tracks=tracklist, request=request)


def parse_playlists_to_get(request: Request, get_to_download=False) -> list[Playlist] | None:
    hitmo_parser = HitmoParser()
    raw_playlists = hitmo_parser.get_playlists(request)
    playlists = hitmo_parser.get_playlist_objects(raw_playlists)

    if get_to_download:
        return playlists
    else:
        request.data['playlists'] = make_music_objects_list_json_response(musobj_list=playlists)


def get_playlist_to_download(request: Request, playlists: list[Playlist]) -> Playlist | None:
    playlist_id = request.query_params.get('playlist_id')
    if playlist_id is not None:
        return playlists[int(playlist_id)-1]
    else:
        return


def parse_playlists_to_download(request: Request):
    hitmo_parser = HitmoParser()

    playlists = parse_playlists_to_get(request, get_to_download=True)
    playlist_to_download = get_playlist_to_download(request, playlists)
    tracks_from_playlist = hitmo_parser.get_tracks_from_musobj(request, musobj=playlist_to_download,
                                                        track_parser=hitmo_parser.parse_and_get_tracks)
    tracks_objs_list = hitmo_parser.get_track_objects_list(tracks=tracks_from_playlist)
    download.download_list_musobj(tracks=tracks_objs_list,
                                                    folder_path=PathManager.download_path / playlist_to_download.title)

    request.data['playlist'] = make_musobj_json_response(musobj=tracks_objs_list)


def parse_albums_to_get(request: Request, get_to_download=False):
    hitmo_parser = HitmoParser()
    raw_albums = hitmo_parser.get_albums(request)
    albums = hitmo_parser.get_album_objects(raw_albums)

    if get_to_download:
        return albums
    else:
        request.data['albums'] = make_music_objects_list_json_response(musobj_list=albums)


def get_album_to_download(request: Request, albums: list[Album]) -> Album | None:
    album_id = request.query_params.get('album_id')
    if album_id is not None:
        return albums[int(album_id) - 1]
    else:
        return


def parse_albums_to_download(request: Request):
    hitmo_parser = HitmoParser()
    albums = parse_albums_to_get(request, get_to_download=True)
    album_to_download = get_album_to_download(request, albums)
    tracks_from_album = hitmo_parser.get_tracks_from_musobj(request, musobj=album_to_download,
                                                               track_parser=hitmo_parser.parse_and_get_tracks)
    tracks_objs_list = hitmo_parser.get_track_objects_list(tracks=tracks_from_album)
    download.download_list_musobj(tracks=tracks_objs_list,
                                                        folder_path=PathManager.download_path / album_to_download.title)

    request.data['album'] = make_musobj_json_response(musobj=tracks_objs_list)


def parse_hitmo(request: Request, parser) -> None:
    hitmo = data.HitmoData()
    Parser.parse_site(request, data_obj=hitmo, parser=parser, logger=logger)
