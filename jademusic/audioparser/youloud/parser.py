import logging

from requests_html import HTMLSession, Element
from rest_framework.request import Request
from rich.console import Console

from audioparser import paths, download
from audioparser.generics.responses import make_music_objects_list_json_response
from audioparser.generics.parser import Parser
from audioparser.youloud.data import YouLoudData

logger = logging.getLogger(__name__)
log_format ='[%(levelname)s] %(asctime)s | %(module)s.%(funcName)s <line %(lineno)d> | %(message)s'
logging.basicConfig(format=log_format, level='INFO')
console = Console()


class YouLoudParser(Parser):
    youloud = YouLoudData()

    def search_albums(self, request, search_value):
        session = HTMLSession()
        response = self.get_site_response(request=request, session=session, url=self.youloud.url)
        response.html.render(reload=False)
        
        # search_form = response.html.find('input#story', first=True)
        # search_form.attrs.value = search_value


def parse_albums_to_download(request: Request):
    pass


def parse_albums_to_get(request: Request):
    parser = YouLoudParser()
    parser.search_albums(request, search_value='Metallica')


def parse_youloud(request: Request, parser) -> None:
    youloud = YouLoudData()
    Parser.parse_site(request, data_obj=youloud, parser=parser, logger=logger)

