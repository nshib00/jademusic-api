# -*- coding: utf-8 -*-


from pathlib import Path
from requests_html import HTMLSession
import requests
from rest_framework.exceptions import APIException
from rich.console import Console
import logging

from rest_framework.request import Request

from . import formatters, paths
from .generics.music_objects import Track

console = Console()
downloading_status = console.status("[bold green]Скачивание треков...")

logger = logging.getLogger(__name__)
log_format ='[%(levelname)s] %(asctime)s | %(module)s.%(funcName)s <line %(lineno)d> | %(message)s'
logging.basicConfig(format=log_format, level='INFO')


def write_track_in_file(track, number_prefix, content):
    logger.info('Called function download.write_track_in_file.')

    try:
        with open(track.path, 'wb') as file:
            file.write(content) 
    except FileNotFoundError as exc:
        logger.error(exc)
        console.print(f'[bold red][Ошибка][/] [yellow]Указана несуществующая папка для загрузки аудиозаписей.[/yellow]')  
    except Exception as exc:
        logger.error(exc)
        console.print(f'[bold red][Ошибка][/] [yellow]Трек "{track.full_title}" не удалось скачать.[/yellow]')
    else:      
        if number_prefix:
            console.print(f'[bold green]{number_prefix}[/][cyan]Трек [italic]{track.full_title}[/italic] успешно скачан.[/]')
        else:
            console.print(f'[bold green]Трек [italic]{track.full_title}[/italic] успешно скачан.[/]')


def download_one_track(folder_path, track, session, track_num=None, tracks_count=None):
    track.full_title = formatters.format_track_title(track.full_title)
    track.path = track.make_path(folder_path, track.full_title)

    if paths.check_track(track.path):
        print(f'Трек {track.full_title} ранее уже был скачан.')
    else:
        try:
            req = session.get(track.url)
            paths.check_folder(folder_path)
            if not req.ok:
                raise APIException(code=req.status_code)
        except APIException as exc:
            logger.error(exc)
            console.print(f'[bold red][Error][/] HTTP {exc.status_code}: {exc.detail}')
        except requests.exceptions.ConnectionError as exc:
            logger.error(exc)
            console.print('[bold red][Error][/] Connection with server lost.')
        else:
            number_prefix = formatters.make_number_prefix(track_num, tracks_count)
            write_track_in_file(track, number_prefix, content=req.content)
            

def download_first_n_tracks(folder_path, session, tracks, tracks_amount):
    console.print('[bold orange]Загрузка первых нескольких треков.[/]')
    for track_number in range(1, tracks_amount+1):
        download_one_track(folder_path=folder_path, track=tracks[track_number-1], 
                            session=session, track_num=track_number-1, tracks_count=tracks_amount)


def download_tracks_by_numbers(folder_path, session, tracks, track_nums):
    console.print('[#ff8000 bold]Загрузка нескольких треков по их номерам.[/]') 
    track_numbers_list = [int(num) for num in track_nums.split(',')]
    for index, track in enumerate(tracks):
        download_one_track(folder_path=folder_path, track=track, 
                        session=session, track_num=index, tracks_count=len(track_numbers_list))


def download_all_tracks(folder_path, session, tracks):
    if isinstance(tracks, list):
        console.print(f'[#ff8000 bold]Будет загружено треков: [/][yellow italic]{len(tracks)}.[/]')
    for index, track in enumerate(tracks):
        download_one_track(folder_path=folder_path, track=track, session=session,
                                                        track_num=index, tracks_count=len(tracks))


def download_tracks(folder_path: Path, tracks: list[Track], request: Request) -> None:
    logger.info('Called function download.download_tracks.')

    session = HTMLSession()
    requested_dmode = request.query_params.get('mode')
    download_mode = 'all' if requested_dmode is None else requested_dmode

    for track in tracks:
        track.validate_url()

    match download_mode:
        case 'first_n':
            download_first_n_tracks(folder_path, session, tracks,
                            tracks_amount=formatters.format_tracks_amount(request.query_params))
        case 'by_numbers':
            download_tracks_by_numbers(folder_path, session, tracks, track_nums=request.query_params['track_nums'])
        case 'all':
            download_all_tracks(folder_path, session, tracks)
        case 'only_one':
            download_one_track(folder_path, track=tracks[0], session=session)


def download_list_musobj(tracks, folder_path): # download album or playlist
    session = HTMLSession()
    download_all_tracks(folder_path, session, tracks)