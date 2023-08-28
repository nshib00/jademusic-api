import re

import requests
from lxml.etree import ParserError
from requests import Response
from requests_html import Element, HTMLSession
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rich.console import Console

from audioparser import paths, exceptions
from audioparser.generics import html as generics_html
from audioparser.generics.music_objects import make_track_object, Track, Playlist, make_playlist_object, \
    make_album_object, Album
from musapi import utils as musapi_utils

console = Console()


class Parser:
    @staticmethod
    def get_site_response(request: Request, url: str, session: HTMLSession) -> Response:
        response = session.get(url)
        request.data['status'] = response.status_code
        return response

    @staticmethod
    def parse_tracks_urls(tracks_html: list[Element]) -> list[str]:
        tracks_urls = []
        for track in tracks_html:
            track_url_html = track.find(generics_html.TRACK_REF_HTML, first=True)
            tracks_urls.append(track_url_html.attrs.get('href'))
        return tracks_urls

    @staticmethod
    def get_tracks_to_download_list(tracks_list: list[Track], request: Request) -> list[Track]:
        tracks_to_download = []
        if request.query_params.get('mode'):
            if request.query_params.get('mode') in Track.GET_AND_DOWNLOAD_METHODS:
                getting_mode = request.query_params.get('mode')
            else:
                methods_string = musapi_utils.make_track_methods_string()
                raise APIException(code=400, detail=f'Некорректный запрос: неверное значение параметра mode: {request.query_params.get("mode")}. Этот параметр должен принимать одно из следующих значений: {methods_string}.')
        else:
            getting_mode = 'all'

        if not tracks_list:
            request.data['status'] = 200
            return []

        match getting_mode:
            case 'first_n':
                n = int(request.query_params['n'])
                tracks_to_download.extend(tracks_list[:n])
            case 'by_numbers':
                track_nums = request.query_params['track_nums']
                for tnum in track_nums.split(','):
                    tracks_to_download.append(tracks_list[int(tnum)-1])
            case 'all':
                return tracks_list
            case 'only_one':
                return [ tracks_list[0] ]
            case _:
                return []
        return tracks_to_download

    def get_album_attrs_dict(self, raw_album):
        pass

    def get_track_objects_list(self, tracks: list[dict]) -> list[Track]:
        track_objects_list = []
        for index, track in enumerate(tracks):
            track_dict = track if isinstance(track, dict) else {}

            track_obj = make_track_object(raw_track=track_dict, track_id=index+1)
            track_objects_list.append(track_obj)
        return track_objects_list

    @staticmethod
    def get_playlist_objects(playlists: list[dict]) -> list[Playlist]:
        playlist_objects = []
        for index, playlist in enumerate(playlists):
            playlist_objects.append(
                make_playlist_object(raw_playlist=playlist, playlist_id=index+1)
            )
        return playlist_objects

    @staticmethod
    def get_album_objects(playlists: list[dict]) -> list[Album]:
        album_objects = []
        for index, album in enumerate(playlists):
            album_objects.append(
                make_album_object(raw_album=album, album_id=index+1)
            )
        return album_objects

    def get_tracks_from_musobj(self, request, musobj: Playlist | Album, track_parser) -> list[dict]:
        session = HTMLSession()
        response = self.get_site_response(request, url=musobj.url, session=session)
        return track_parser(response)

    @staticmethod
    def get_pages_count(request: Request) -> int:
        if request.query_params.get('pages'):
            pages_count = request.query_params['pages']
        else:
            pages_count = 1
        return pages_count

    @staticmethod
    def check_request_folder(request: Request) -> None:
        if request.query_params.get('folder'):
            paths.check_folder(request.query_params['folder'])
            paths.change_download_path(new_path=request.query_params['folder'])


    @staticmethod
    def find_artist_page_url(query_url, urls):
        query = re.search(r'\?q=[\w\W]+', query_url).group(0)[3:]
        filtered_query = query.replace('+', ' ')

        for url in urls:
            if re.search(pattern=filtered_query.lower(), string=url.text.lower()):
                return url
            else:
                if re.findall(pattern=filtered_query.lower(), string=url.text.lower()):
                    return url

    def get_artist_page_url(self, query_url: str, artist_html: str) -> str | None:
        session = HTMLSession()
        response = session.get(query_url)

        urls_list = response.html.find(artist_html)
        artist_page_url = self.find_artist_page_url(query_url, urls=urls_list)
        if artist_page_url:
            return artist_page_url.attrs.get('href')

    @staticmethod
    def get_page(request):
        page = request.query_params.get('page')
        if page is not None:
            return int(page)
        return 1

    @staticmethod
    def parse_site(request, data_obj, parser, logger):
        try:
            parser(request)
        except requests.ConnectionError as exc:
            connection_error_message = 'Скачать музыку не удалось. Проверьте подключение к интернету.'
            exceptions.handle_exception(request, logger, exc, console,
                                        error_msg=connection_error_message, http_status=504)
        except ParserError as exc:
            parser_error_message = 'Ошибка парсера: искомая страница не найдена.'
            # parser_error_message = f'Ошибка парсера: по URL {data_obj.url} искомый сайт не был найден. Возможно, сайт не работает или сменил домен.'
            exceptions.handle_exception(request, logger, exc, console, error_msg=parser_error_message,
                                         http_status=404)
        except Exception as exc:
            exceptions.handle_exception(request, logger, exc, console, http_status=500)
            x = 0

