import requests

from django.conf import settings


class RSSFeedClient:

    @classmethod
    def get_rss_feed(cls):
        params = {
            'rss_url': settings.NOTICIAS_RSS_FEED_URL
        }
        items = requests.get(settings.RSS_TO_JSON_URL, params=params).json()['items']
        return [
            {
                'date': item['pubDate'],
                'title': item['title'],
                'description': item['description'],
                'content': item['content'],
            } for item in items
        ]
