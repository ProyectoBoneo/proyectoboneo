import logging
from bs4 import BeautifulSoup

from rest_framework.response import Response
from rest_framework.views import APIView

from proyecto_boneo.apps.api.noticias.client import RSSFeedClient

logger = logging.getLogger(__name__)


NOTICIAS_SAMPLE = [
    {
        "date": "2018-08-28 23:34:22",
        "title": "Temporada de mariposas",
        "description": "Comienza la temporada de mariposas Nuestro patio tiene varias",
        "content": "Comienza la temporada de mariposas\nNuestro patio tiene varias",
        "images": [
            "http://localhost:8000/static/noticias/butterfly.jpg"
        ]
    },
    {
        "date": "2018-08-28 23:32:26",
        "title": "Festival musical en la escuela",
        "description": "Este es un post sobre un festival musical de la escuela",
        "content": "Este es un post sobre un festival musical de la escuela",
        "images": [
            "http://localhost:8000/static/noticias/guitar.jpg"
        ]
    },
    {
        "date": "2018-08-28 23:26:37",
        "title": "Se prepara la jornada educativa",
        "description": "Habrá una jornada educativa Presentamos una imagen en alta resolución Esta imagen muestra una linda ciudad",
        "content": "Habrá una jornada educativa\nPresentamos una imagen en alta resolución\nEsta imagen muestra una linda ciudad",
        "images": [
            "http://localhost:8000/static/noticias/edificio.jpg"
        ]
    },
    {
        "date": "2018-08-28 23:24:35",
        "title": "Don Orione",
        "description": "Este es un post sobre don Orione. Aquí adjunto una imagen.",
        "content": "Este es un post sobre don Orione.\nAquí adjunto una imagen.",
        "images": [
            "http://localhost:8000/static/noticias/orione.jpg"
        ]
    }
]


class NoticiasView(APIView):

    def _get_rss_feed(self):
        content = []
        feed_items = RSSFeedClient().get_rss_feed()
        for item in feed_items:
            soup = BeautifulSoup(item['content'], 'html.parser')
            paragraphs = soup.find_all('p')
            content_lines = []
            images = []
            for paragraph in paragraphs:
                for child in paragraph.children:
                    if isinstance(child, str):
                        content_lines.append(child.strip())
                    elif child.name == 'img':
                        images.append(child.attrs['data-orig-file'])
            item['content'] = '\n'.join(content_lines).strip()
            item['images'] = images
            content.append(item)
        return content

    def _get_sample_rss_feed(self):
        pass

    def get(self, request, *args, **kwargs):
        try:
            content = self._get_rss_feed()
        except Exception:
            logger.info('There was an error while fetching the rss feed. Using default content')
            content = NOTICIAS_SAMPLE
        return Response(content)
