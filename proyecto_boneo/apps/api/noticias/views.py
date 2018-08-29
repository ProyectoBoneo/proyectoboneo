from bs4 import BeautifulSoup

from rest_framework.response import Response
from rest_framework.views import APIView

from proyecto_boneo.apps.api.noticias.client import RSSFeedClient


class NoticiasView(APIView):

    def get(self, request, *args, **kwargs):
        response = []
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
            response.append(item)
        return Response(response)
