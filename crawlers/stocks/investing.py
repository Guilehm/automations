from scrapy import Selector
from crawlers.utils import BaseSpider


BASE_CRAWLER_URL = 'https://br.investing.com'


class InvestingSpider(BaseSpider):
    def __init__(self, base_url=BASE_CRAWLER_URL, *args, **kwargs):
        super().__init__(base_url, *args, **kwargs)
