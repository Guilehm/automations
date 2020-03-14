from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from driver.driver_builder import Driver

BASE_URL = 'https://www.submarinoviagens.com.br'


class SubmarinoFlightsCrawler:

    def __init__(self, headless=False, url=BASE_URL):
        self.url = url
        self.driver = Driver(headless=headless).get_driver()
        self._get_page()

    def _get_page(self):
        self.driver.get(self.url)

    def find_by_id(self, _id):
        return self.driver.find_element_by_id(_id)

    def fill_origin_input(self, airport_code='CGH'):
        self.driver.find_element_by_xpath('//p[@class="cidade"]').click()
        origin_input = self.find_by_id(_id='pesqinc')
        origin_input.send_keys(airport_code)