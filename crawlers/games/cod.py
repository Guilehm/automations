from scrapy import Selector

from crawlers.utils import BaseSpider

BASE_CRAWLER_URL = 'https://cod.tracker.gg/warzone/profile/{platform}/{username}/overview'
BASE_API_URL = 'https://api.tracker.gg/api/v2/warzone/standard/profile/{platform}/{username}'


class CodCrawler(BaseSpider):
    def __init__(self, base_url=BASE_CRAWLER_URL, *args, **kwargs):
        super().__init__(base_url, *args, **kwargs)

    def get_response(self, platform, username):
        self._validate_request(platform, username)
        self.response = Selector(text=self._response.text)
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

        return dict(
            playTime=play_time,
            matches=matches,
            rankIcon=rank_icon,
            level=level,
            progression=progression,
        )


class CodAPI(BaseSpider):
    def __init__(self, base_url=BASE_API_URL, *args, **kwargs):
        super().__init__(base_url, *args, **kwargs)

    def get_response(self, platform, username, save=False):
        self._validate_request(platform, username)
        self.response = self._response.json()
        if save:
            self.save_data(
                collection='profile',
                data=self.response,
            )
        return self.response
