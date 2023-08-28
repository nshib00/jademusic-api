import logging
import random
import re

from requests_html import HTMLSession, Element
from rest_framework.request import Request
from rich.console import Console

from audioparser import paths, download
from audioparser.generics.responses import make_music_objects_list_json_response
from audioparser.generics.parser import Parser
from audioparser.mp3party import data
from audioparser.mp3party.data import Mp3PartyData

logger = logging.getLogger(__name__)
log_format ='[%(levelname)s] %(asctime)s | %(module)s.%(funcName)s <line %(lineno)d> | %(message)s'
logging.basicConfig(format=log_format, level='INFO')
console = Console()


class Mp3PartyParser(Parser):
    mp3party = Mp3PartyData()

    def get_track_attrs_dict(self, track: Element) -> dict[str]:
        track_id = track.attrs.get('data-js-id')
        server_num = random.randint(1, 2)

        return {
            'id': int(track_id),
            'artist': track.attrs.get('data-js-artist-name'),
            'title': track.attrs.get('data-js-song-title'),
            'image': self.mp3party.image_url + str(track.attrs.get('data-js-image')),
            'url': f'https://dl{server_num}.' + self.mp3party.download_url + track_id,
        }

    @staticmethod
    def get_album_full_title(raw_album: Element):
        title, artist = raw_album.text.split('\n')
        return f'{artist} - {title}'

    @staticmethod
    def get_album_url(raw_album: Element):
        for url in raw_album.absolute_links:
            if re.search(r'albums\/\d+', url):
                return url

    @staticmethod
    def get_album_id(album_url):
        album_id = re.findall(r'\d+', album_url)
        return int(album_id[-1])

    def get_album_attrs_dict(self, raw_album: Element) -> dict[str]:
        album_url = self.get_album_url(raw_album)
        return {
            'id': self.get_album_id(album_url),
            'title': self.get_album_full_title(raw_album),
            'url': album_url,
        }

    def get_tracks_list(self, request, query=None, pages=1, is_popular=False, new_music=False, artist_url=None) -> list[dict]:
        tracks_list = []
        session = HTMLSession()

        for page_num in range(pages):
            if not is_popular:
                if artist_url is not None:
                    url = artist_url
                else:
                    url = self.mp3party.search_url + query
            else:
                url = self.mp3party.popular_tracks_url
            response = self.get_site_response(request, url, session)
            tracks_html = response.html.find('div.track__user-panel')

            for track in tracks_html:
                tracks_list.append(
                    self.get_track_attrs_dict(track)
                )
        return tracks_list

    def get_genres(self, request) -> dict:
        session = HTMLSession()
        genres_dict = {}
        genres_page = self.get_site_response(request, self.mp3party.genres_url, session)
        genres_html = genres_page.html.find('a.genre-list__link')

        for genre in genres_html:
            genres_dict[genre.text] = genre.absolute_links.pop()
        return genres_dict

    def get_subgenres(self, request, genre_page_url) -> dict:
        subgenres_dict = {}
        session = HTMLSession()
        genre_page = self.get_site_response(request, genre_page_url, session)
        subgenres = genre_page.html.find('div.carousel__interface', first=True).find('li.carousel__slide')
        for subg in subgenres:
            subgenres_dict[subg.text] = subg.absolute_links.pop()
        return subgenres_dict

    def get_genre_albums(self, request, genre_url):
        session = HTMLSession()
        genre_page = self.get_site_response(request, genre_url, session)
        genre_albums = genre_page.html.find('div.carousel__slides', first=True).find('div.carousel__slide')
        genre_albums_list = []
        for album in genre_albums:
            genre_albums_list.append(self.get_album_attrs_dict(album))
        return genre_albums_list


def parse_tracks_to_get(request: Request, get_to_download=False):
    mp3party_parser = Mp3PartyParser()
    pages_count = mp3party_parser.get_pages_count(request)

    if request.query_params.get('popular_tracks'):
        tracks_list = mp3party_parser.get_tracks_list(request, is_popular=True)
    elif request.query_params.get('new_tracks'):
        tracks_list = mp3party_parser.get_tracks_list(request, new_music=True)
    else:
        query = request.query_params.get('q')
        tracks_list = mp3party_parser.get_tracks_list(request, query=query, pages=pages_count)
        filtered_tracks_list = mp3party_parser.get_tracks_to_download_list(tracks_list, request)

    if len(tracks_list) == 0:
        console.print('[#ffff00 bold]По вашему запросу ничего не найдено. Проверьте, не ошиблись ли в названии трека/исполнителя и попробуйте еще раз.\n[/]')
        request.data['tracks'] = []
    else:
        tracklist = mp3party_parser.get_track_objects_list(filtered_tracks_list)
        print('Найдено треков:', len(tracklist))

        request.data['tracks'] = make_music_objects_list_json_response(musobj_list=tracklist)

        if get_to_download:
            mp3party_parser.check_request_folder(request)
            return tracklist


def parse_tracks_to_download(request: Request):
    tracklist = parse_tracks_to_get(request, get_to_download=True)
    download.download_tracks(folder_path=paths.download_path, tracks=tracklist, request=request)


def parse_albums_to_get(request: Request, get_to_download=False):
    mp3party_parser = Mp3PartyParser()

    if get_to_download:
        mp3party_parser.check_request_folder(request)


def parse_albums_to_download(request: Request) -> None:
    mp3party_parser = Mp3PartyParser()

    if request.query_params.get('genre'):
        genre_page_url = mp3party_parser.mp3party.genres_url + '/' + request.query_params.get('genre')
        genres = mp3party_parser.get_genres(request)
        if request.query_params.get('genre_albums'):
            genre_albums = mp3party_parser.get_genre_albums(request, genre_page_url)
    if request.query_params.get('subgenre'):
        subgenres = mp3party_parser.get_subgenres(request, genre_page_url)

    # if request.query_params.get('album'):
    #     download.download_album(folder_path=paths.download_path)


def parse_playlists_to_dowload(request: Request) -> None:
    pass


def parse_playlists_to_get(request: Request) -> None:
    pass


def parse_mp3party(request: Request, parser) -> None:
    mp3party = data.Mp3PartyData()
    Parser.parse_site(request, data_obj=mp3party, parser=parser, logger=logger)

