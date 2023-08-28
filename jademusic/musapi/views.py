from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework import status

from audioparser.generics import main_parser
from musapi.models import JadeMusicUser
from musapi.serializers import JadeMusicUserSerializer

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

import logging


logger = logging.getLogger(__name__)
log_format ='[%(levelname)s] %(asctime)s | %(module)s.%(funcName)s <line %(lineno)d> | %(message)s'
logging.basicConfig(format=log_format, level='INFO')


class BaseMusapiView(APIView):
    '''
    Parent view for all track, album and playlist views.
    '''
    def get(self, request, parser, *args, **kwargs):
        try:
            parser(request, *args, **kwargs)
        except APIException as exc:
            return Response(
                data={
                    'data': request.data,
                    'error_detail': exc.detail,
                    },
                status=exc.status_code
            )
        except Exception as exc:
            return Response(
                data={
                    'error': exc,
                    'data': exc.args
                },
                status=500
            )
        return Response(data={'data': request.data}, status=status.HTTP_200_OK)


class TrackDownloadView(BaseMusapiView):
    '''
    View for downloading tracks from site "Hitmo".
    URL params:
        user request. may contain the name of the artist or track. This param should not be used with the params "popular" and "new".
        popular - param for downloading tracks from popular tracks page. Values: 0, 1. Default: 0. Should be used instead of "q" param. This param should not be used with the "new" param.
        new - param for downloading tracks from page "New music for today". Values: 0, 1. Default: 0. Should be used instead of "q" param. This param should not be used with the "popular" param.
        mode - option to select specific group of tracks to download. Values: only_one, by_numbers, first_n, all.
            only_one - first track in list of found tracks will be downloaded.
            first_n - first N tracks in list of found tracks will be downloaded.
            by_numbers - several tracks will be downloaded by their numbers in the list. Аll required track numbers
                must be on one line, each number is separated by a comma without a space. Numbers can be placed
                in any order.
                Example: 1,3,7,8,5,14,10
            all - all tracks from the list will be downloaded.
        artist - option to download tracks of a specific artist from his page on the site. Values: 0, 1.
            0 - tracks will download from search menu. With this value, the track list may contain tracks
                of other artists with a similar name.
            1 - tracks will download from artist page on site.
    '''
    def get(self, request, *args, **kwargs):
        return super().get(request, parser=main_parser.start_track_parser, action='download')


class TrackGetView(BaseMusapiView):
    '''
    View for getting tracks from site "Hitmo".
    URL params:
        q - user request. may contain the name of the artist or track. This param should not be used with the params
        "popular" and "new".
        popular - param for getting tracks from popular tracks page. Values: 0, 1. Default: 0. Should be used instead of
        "q" param. This param should not be used with the "new" param.
        new - param for getting tracks from page "New music for today". Values: 0, 1. Default: 0. Should be used instead
        of "q" param. This param should not be used with the "popular" param.
        artist - option to get tracks of a specific artist from his page on the site. Values: 0, 1.
            0 - tracks will be taken from search menu. With this value, the track list may contain tracks
                of other artists with a similar name.
            1 - tracks will be taken from artist page on site.
    '''
    def get(self, request, *args, **kwargs):
        return super().get(request, parser=main_parser.start_track_parser, action='get', *args, **kwargs)


class AlbumDownloadView(BaseMusapiView):
    '''
    View for downloading albums from site "MP3Party".
    '''
    def get(self, request, *args, **kwargs):
        return super().get(request, parser=main_parser.start_album_parser, action='download', *args, **kwargs)


class AlbumGetView(BaseMusapiView):
    '''
    View for getting albums from site "MP3Party".
    '''
    def get(self, request, *args, **kwargs):
        return super().get(request, parser=main_parser.start_album_parser, action='get', *args, **kwargs)


class PlaylistDownloadView(BaseMusapiView):
    '''
    View for downloading playlists from site "Hitmo".
    '''
    def get(self, request, *args, **kwargs):
        return super().get(request, parser=main_parser.start_playlist_parser, action='download', *args, **kwargs)


class PlaylistGetView(BaseMusapiView):
    '''
    View for getting playlists from site "Hitmo".
    '''
    def get(self, request, *args, **kwargs):
        return super().get(request, parser=main_parser.start_playlist_parser, action='get', *args, **kwargs)


class RegisterUserView(CreateAPIView):
    queryset = JadeMusicUser.objects.all()
    serializer_class = JadeMusicUserSerializer


class CheckUserRegistrationView(APIView):
    def get(self, request):
        user_id = int(request.query_params['user_id'])
        if JadeMusicUser.objects.all():
            if JadeMusicUser.objects.get(telegram_user_id=user_id):
                return Response({'user_id': user_id, 'is_registered': True})
        return Response({'user_id': user_id, 'is_registered': False})


class ListUserView(ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = JadeMusicUser.objects.all()
    serializer_class = JadeMusicUserSerializer


class DetailUserView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = JadeMusicUser.objects.all()
    serializer_class = JadeMusicUserSerializer


class CreateUserTokenView(APIView):
    '''
    View for creating tokens for token authentication.
    '''
    def get(self, request):
        try:
            for user in User.objects.all():
                Token.objects.get_or_create(user=user)
            return Response({'ok': True})
        except Exception as exc:
            error_msg = f'Error occured. {exc.__class__.__name__}: {exc}'
            logger.error(error_msg)
            return Response({'ok': False, 'reason': error_msg})



