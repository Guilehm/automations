import time
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

    def wait_for_element(self, condition, value, timeout=5):
        return WebDriverWait(
            driver=self.driver,
            timeout=timeout,
        ).until(expected_conditions.presence_of_element_located(
            (condition, value,)
        ))

    def _get_page(self):
        self.driver.get(self.url)

    def _fill_airport_input(self, airport_code, target):
        if target not in 'origem destino'.split():
            raise Exception('Target not valid')
        self.driver.find_element_by_xpath(
            f'//div[@class="{target or "destino"}"]/p[@class="cidade"]'
        ).click()
        origin_input = self.driver.find_element_by_id('pesqinc')
        origin_input.send_keys(airport_code)

    def _click_first_result(self):
        first_item_xpath = '//div[@class="resultado"]/ul/li/div[@class="item"]'
        try:
            self.wait_for_element(By.XPATH, first_item_xpath, 15)
        except TimeoutException:
            raise
        self.driver.find_element_by_xpath(first_item_xpath).click()

    def set_airport(self, airport_code='CGH', target='origem'):
        self._fill_airport_input(airport_code, target)
        self._click_first_result()

    def _click_date_input(self):
        self.driver.find_element_by_xpath(
            '//div[@class="motor"]/div[@class="data"]'
        ).click()

    def _click_next_month(self):
        next_month_xpath = '//*[@aria-label="Move forward to switch to the next month."]'
        self.driver.find_element_by_xpath(next_month_xpath).click()

    def find_month(self, month, year):
        time.sleep(1)
        elements = self.driver.find_elements_by_xpath(
            '//div[@class="CalendarMonth CalendarMonth_1"]/div[@class="CalendarMonth_caption CalendarMonth_caption_1"]'
        )[:2]
        desired_month = f'{month} {int(year)}'.upper()
        for element in elements:
            if element.text and element.text.strip() == desired_month:
                break
        else:
            self._click_next_month()
            self.find_month(month, year)
