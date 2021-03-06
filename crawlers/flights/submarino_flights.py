import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from crawlers.flights.utils import get_date
from driver.driver_builder import Driver

BASE_URL = 'https://www.submarinoviagens.com.br'


class SubmarinoFlightsCrawler:

    def __init__(self, headless=False, url=BASE_URL):
        self.url = url
        self.driver = Driver(headless=headless).get_driver()
        self.date_clicked = False
        self.month_element_selected = None
        self.desired_month = None
        self.only_going = False
        self._get_page()

    def wait_for_element(self, condition, value, timeout=5):
        return WebDriverWait(
            driver=self.driver,
            timeout=timeout,
        ).until(expected_conditions.presence_of_element_located(
            (condition, value)
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

    def set_airport(self, *airports):
        targets = {
            0: 'origem',
            1: 'destino',
        }
        for number, code in enumerate(airports[:2]):
            time.sleep(0.5)
            self._fill_airport_input(code, targets.get(number))
            self._click_first_result()

    def _click_date_input(self):
        self.driver.find_element_by_xpath(
            '//div[@class="motor"]/div[@class="data"]'
        ).click()
        self.date_clicked = True

    def _click_next_month(self):
        next_month_xpath = '//*[@aria-label="Move forward to switch to the next month."]'
        self.wait_for_element(By.XPATH, next_month_xpath)
        self.driver.find_element_by_xpath(next_month_xpath).click()

    def _get_first_months(self, number=None):
        elements = self.driver.find_elements_by_xpath(
            '//div[@class="CalendarMonth CalendarMonth_1"]'
        )
        return elements[number] if number else elements[:2]

    def _get_first_months_caption(self):
        return self.driver.find_elements_by_xpath(
            '//div[@class="CalendarMonth CalendarMonth_1"]/'
            'div[@class="CalendarMonth_caption CalendarMonth_caption_1"]'
        )

    def _find_month(self, month, year):
        if not self.date_clicked:
            self._click_date_input()
        time.sleep(1)
        desired_month = f'{month} {int(year)}'.upper()
        elements = self._get_first_months_caption()
        for number, element in enumerate(elements):
            if element.text and element.text.strip() == desired_month:
                self.month_element_selected = number
                break
        else:
            self._click_next_month()
            self._find_month(month, year)

    def _click_day(self, day):
        month_element = self._get_first_months(self.month_element_selected)
        month_element.find_element_by_xpath(f'.//*[text() = "{day}"]').click()
        return month_element

    def _click_apply_date(self):
        self.driver.find_element_by_xpath('//button[@class="btn-web-apply"]').click()

    def _search(self):
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//button[@class="btn-text btn-buscar"]').click()

    def _set_only_going(self):
        element = self.driver.find_element_by_xpath('//div[@class="menu-motor-aero"]/div[@class="item"]')
        ActionChains(self.driver).move_to_element_with_offset(element, 10, 10).click().perform()
        self.only_going = True

    def search_results(self, going_date, returning_date=None):
        if not returning_date:
            self._set_only_going()
        g_year, g_month, g_day = get_date(going_date)
        self._find_month(month=g_month, year=g_year)
        self._click_day(g_day)
        if returning_date:
            r_year, r_month, r_day = get_date(returning_date)
            if g_month == r_month and g_year == r_year:
                self._click_day(r_day)
            else:
                self._find_month(month=r_month, year=r_year)
                self._click_day(r_day)
        self._click_apply_date()
        self._search()

    def get_card_data(self):
        def _parse_card_data(card):
            times = card.find_elements_by_xpath('.//div[@class="c56"]/span[@class="c58"]')
            r_departure_time, r_arrival_time = None, None
            if not self.only_going:
                g_departure_time, g_arrival_time, r_departure_time, r_arrival_time = times
            else:
                g_departure_time, g_arrival_time = times
            card_data = dict(going=dict(
                departureTime=g_departure_time.text,
                arrivalTime=g_arrival_time.text,
            ))
            if not self.only_going:
                card_data.update(returning=dict(
                    departureTime=r_departure_time.text,
                    arrivalTime=r_arrival_time.text,
                ))
            return card_data

        cards_xpath = '//div[@class="c16"]/div[@class="c18 c19"]'
        try:
            self.wait_for_element(By.XPATH, cards_xpath, 30)
        except TimeoutException:
            raise TimeoutException(f'Could not find xpath: {cards_xpath}')
        cards = self.driver.find_elements_by_xpath(cards_xpath)
        return (_parse_card_data(card) for card in cards)

    def get_checkout_data(self):
        def _parse_checkout_data(checkout):
            # TODO: parse price
            return dict(
                passengers=checkout.find_element_by_xpath('./div/p[@class="qtd-passageiros"]').text,
                price=checkout.find_element_by_xpath('./div/p[@class="valor-total"]').text,
            )
        checkouts_xpath = '//div[@class="total-checkout"]'
        try:
            self.wait_for_element(By.XPATH, checkouts_xpath, 30)
        except TimeoutException:
            raise
        checkouts = self.driver.find_elements_by_xpath(checkouts_xpath)
        return (_parse_checkout_data(checkout) for checkout in checkouts)


c = SubmarinoFlightsCrawler()
c.set_airport('RAO', 'CGH')
c.search_results('2020-06-12', '2020-09-12')
# c.search_results('2020-06-12')
c.get_card_data()
c.get_checkout_data()
