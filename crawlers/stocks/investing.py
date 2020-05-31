from datetime import datetime, timedelta

import requests
from requests import RequestException
from scrapy import Selector

from crawlers.utils import BaseSpider
from driver.driver_builder import USER_AGENT

BASE_CRAWLER_URL = 'https://br.investing.com'


class InvestingSpider(BaseSpider):
    def __init__(self, base_url=BASE_CRAWLER_URL, *args, **kwargs):
        super().__init__(base_url, *args, **kwargs)
        self.url = None

    @staticmethod
    def _make_headers(**kwargs):
        headers = {'User-Agent': USER_AGENT, **kwargs}
        return headers

    @staticmethod
    def _make_overview_endpoint_url(category, stock):
        endpoint = f'{category}/{stock}'
        return endpoint

    @staticmethod
    def extract_from_text_or_link(data):
        for value in data:
            link = value.xpath('.//a')
            if link:
                yield dict(text=link.xpath('.//text()').get(), href=link.attrib['href'])
                continue
            yield value.xpath('.//text()').get('')

    def get_response(self, endpoint, force_update=False):
        url = f'{self.base_url}/{endpoint}'
        if self.response and self.url == url and not force_update:
            return self.response
        response = requests.get(url, headers=self._make_headers())
        try:
            response.raise_for_status()
        except RequestException:
            raise
        self.url = url
        self._response = response
        self.response = Selector(text=self._response.text)
        return self.response

    def _get_main_info(self):
        response = self.response
        name = response.xpath('//h1/text()').get('').strip()
        ticker = response.xpath('//meta[@itemprop="tickerSymbol"]/@content').get()
        # TODO: format value
        value = response.xpath('//*[@id="last_last"]/text()').get()
        time = datetime.utcnow() - timedelta(hours=3)
        return dict(
            name=name,
            ticker=ticker,
            value=value,
            time=time.isoformat(),
            timestamp=datetime.timestamp(time),
            url=self.url,
        )

    def _get_overview_table_data(self):
        response = self.response
        base_xpath = '//div[@class="clear overviewDataTable overviewDataTableWithTooltip"]//span[@class="{}"'
        titles = response.xpath(f'{base_xpath.format("float_lang_base_1")}]/text()').getall()
        values_xpath = response.xpath(f'{base_xpath.format("float_lang_base_2 bold")}]')
        values = self.extract_from_text_or_link(values_xpath)
        return {title: value for title, value in zip(titles, values)}

    def get_overview_data(self, category='equities', stock='via-varejo-sa', force_update=False):
        endpoint = self._make_overview_endpoint_url(category, stock)
        self.get_response(endpoint, force_update=force_update)
        main_info = self._get_main_info()
        overview_data = self._get_overview_table_data()
        return {**main_info, 'overviewData': overview_data}
