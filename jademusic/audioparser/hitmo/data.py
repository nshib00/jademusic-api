from audioparser.hitmo.url import get_hitmo_url

hitmo_root_url = get_hitmo_url()[:-1]
PAGINATION_SUFFIX = 'start/'


class HitmoData:
    url = hitmo_root_url
    search_url = hitmo_root_url + '/search?q='
    pagination_search_url = hitmo_root_url + f'/search/{PAGINATION_SUFFIX}'
    popular_tracks_url = hitmo_root_url + '/songs/top-today'
    playlists_url = hitmo_root_url + '/collections'
    albums_url = hitmo_root_url + '/albums'
    new_tracks_url = hitmo_root_url + '/songs/new'

    @staticmethod
    def get_tracks_pagination_url(page=1, artist_url=None): # нумерация страниц с нуля
        if artist_url is not None:
            return f'{artist_url}/{PAGINATION_SUFFIX}{48*(page-1)}'
        return HitmoData.pagination_search_url + f'{48*(page-1)}?q='

    def get_albums_pagination_url(self, page=1):
        return f'{self.albums_url}/{PAGINATION_SUFFIX}{40 * (page-1)}'

    def get_playlists_pagination_url(self, page=1):
        return f'{self.playlists_url}/{PAGINATION_SUFFIX}{52 * (page-1)}'
