import requests
from requests import RequestException
from scrapy import Selector

from crawlers.utils import BaseSpider
from driver.driver_builder import USER_AGENT

BASE_CRAWLER_URL = 'https://br.investing.com'


class InvestingSpider(BaseSpider):
    def __init__(self, base_url=BASE_CRAWLER_URL, *args, **kwargs):
        super().__init__(base_url, *args, **kwargs)

    @staticmethod
    def _make_headers(**kwargs):
        headers = {'User-Agent': USER_AGENT, **kwargs}
        return headers

    def get_response(self, endpoint):
        url = f'{self.base_url}/{endpoint}'
        response = requests.get(url, headers=self._make_headers())
        try:
            response.raise_for_status()
        except RequestException:
            raise
        self._response = response
        self.response = Selector(text=self._response.text)
        return self.response

    def parse_overview_data_table(self, category='equities', stock='via-varejo-sa'):
        endpoint = f'{category}/{stock}'
        response = self.get_response(endpoint)
        base_xpath = '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]//span[@class="{}"]/text()'
        titles = response.xpath(base_xpath.format('float_lang_base_1')).getall()
        values = response.xpath(base_xpath.format('float_lang_base_2 bold')).getall()
        return {title: value for title, value in zip(titles, values)}
