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
        self.response = Selector(text=response.text)
        return self.response

    def _parse_overview_data(self):
        response = self.response
        details_xpath = '//div[@class="title"]/div//span[@class="{info}"]//text()'
        play_time = response.xpath(details_xpath.format(info='playtime')).get().strip()
        matches = response.xpath(details_xpath.format(info='matches')).get().strip()

        highlighted_xpath = '//div[@class="highlighted"]'
        progression_xpath = f'{highlighted_xpath}/div[@class="highlighted__stat highlighted__stat--progression"]'
        rank_icon = response.xpath(f'{progression_xpath}//img/@src').get()
        level = response.xpath(f'{progression_xpath}//div[@class="highlight-text"]/text()').get().strip()
        progression = response.xpath(f'{progression_xpath}//span[@class="progression"]//text()').get()

        return (dict(
            playTime=play_time,
            matches=matches,
            rankIcon=rank_icon,
            level=level,
            progression=progression,
        ))

