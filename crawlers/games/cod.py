import requests
from requests import RequestException
from scrapy import Selector

BASE_URL = 'https://cod.tracker.gg/warzone/profile/{platform}/{username}/overview'


class CodCrawler:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.response = None

    def get_response(self, platform, username):
        url = self.base_url.format(
            platform=platform,
            username=username,
        )
        response = requests.get(url)
        try:
            response.raise_for_status()
        except RequestException:
            raise
        return Selector(text=response.text)
