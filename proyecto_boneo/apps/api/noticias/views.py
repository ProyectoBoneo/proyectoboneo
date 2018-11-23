import logging
from bs4 import BeautifulSoup

from rest_framework.response import Response
from rest_framework.views import APIView

from proyecto_boneo.apps.api.noticias.client import RSSFeedClient

logger = logging.getLogger(__name__)


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
        except Exception as e:
            logger.error('There was an error while fetching the rss feed', e)
            content = self._get_sample_rss_feed()
        return Response(content)
