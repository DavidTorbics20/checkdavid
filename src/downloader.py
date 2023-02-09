"""Everything that happens behind the scenes is in here.
   The website I will be gettint the flight information from
   is https://tarkov-market.com/."""

import sys
import time

import parse
from bs4 import BeautifulSoup as BS
from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Downloader():
    def __init__(self, url) -> None:
        self.base_url = "https://tarkov-market.com/"
        self.url = self.base_url + url

    def get_page_content(self):
        """Get the html file of a website."""

        """First create the webdriver and change some options."""
        options = webdriver.ChromeOptions()
        options.add_argument("start-minimized")
        options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(self.url)

        """The "Load more" Buttons location in the hierarchy."""
        initial_XPATH = '//*[@id="__layout"]/div/div/div[2]/div[2]/button'

        max_click_SHOW_MORE = 150
        count = 0

        driver.execute_script("window.scrollTo(0," +
                              "document.body.scrollHeight)")
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, initial_XPATH))).click()  # noqa: E501
        last_height = 0

        while count < max_click_SHOW_MORE:
            print("Scroll down: " + str(last_height))
            driver.execute_script("window.scrollTo(0," +
                                  "document.body.scrollHeight)")
            new_height = driver.execute_script("return document." +
                                               "body.scrollHeight")
            time.sleep(0.5)
            if new_height == last_height:
                break

            last_height = new_height

            try:
                new_XPATH = initial_XPATH[:67] + str(count) + initial_XPATH[67:]
                WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, new_XPATH))).click()  # noqa: E501
            except TimeoutException:
                pass

            count += 1

        original_stdout = sys.stdout

        with open('webpage.html', 'w', encoding='utf-8') as f:

            sys.stdout = f
            print(driver.page_source.encode("utf-8"))
            sys.stdout = original_stdout

        driver.quit()
        print("Finished download")

    def extract_values(self, filename):

        position = 2

        items = []
        prices = []
        prices_per_slot = []
        h_changes = []
        d_changes = []
        trader_prices = []
        trader_names = []

        with open(filename, 'r') as f:
            soup = BS(f.read(), "html.parser")
            dom = etree.HTML(str(soup))

            while True:
                if dom.xpath("/html/body/div/div/div/div/div[2]/" +
                             "div[2]/div[5]/div[" + str(position) + "]/div[1]/a") == []:
                    break

                xpath_start = "/html/body/div/div/div/div/div[2]/div[2]/div[5]/div["

                item_XPATW = xpath_start + str(position) + "]/div[1]/a"
                price_XPATH = xpath_start + str(position) + "]/div[4]/div/span"
                price_per_slot_XPATH = xpath_start + str(position) + "]/div[4]/div/span[2]"
                h_change_XPATH = xpath_start + str(position) + "]/div[5]"
                d_change_XPATH = xpath_start + str(position) + "]/div[6]"
                trader_price_XPATH = xpath_start + str(position) + "]/div[7]/div/div[1]"
                trader_name_XPATH = xpath_start + str(position) + "]/div[7]/div/div[2]"

                item = dom.xpath(item_XPATW)[0].attrib
                items.append(item)
                prices.append(dom.xpath(price_XPATH)[0].text)
                prices_per_slot.append(dom.xpath(price_per_slot_XPATH))
                h_changes.append(dom.xpath(h_change_XPATH)[0].text)
                d_changes.append(dom.xpath(d_change_XPATH)[0].text)
                trader_prices.append(dom.xpath(trader_price_XPATH))
                trader_names.append(dom.xpath(trader_name_XPATH))
                position += 1

        extracted_values = zip(items,
                               prices,
                               prices_per_slot,
                               h_changes,
                               d_changes,
                               trader_prices,
                               trader_names)

        return extracted_values

    def get_values_from_extraction(self, item):
        """
        There is a problem with the name where it
        sometimes just does not parse correctly."""

        # for the name use item[0]
        name = parse.parse("{'class': 'item-img', 'data-v-4e0a3d14': ''," +
                           " 'href': '{}', 'title': '{}'}", str(item[0]).replace("\\", ""))
        if name is not None:
            name = name.fixed[1]

        # for the price use item[1]
        unsigned = item[1].split('\\')[0]

        # for the price per slot use item[2]
        if item[2] != []:
            number_of_slots = parse.parse("{'class': 'price-sec', 'data-v-4e0a3d14': ''," +
                                          " 'title': 'Price per Slot (slots: " +
                                          "{})'}", str(item[2][0].attrib))
            slot_price = int(int(unsigned.replace(',', "")) / int(number_of_slots[0]))
        else:
            slot_price = unsigned

        # for the h_change use item[3]
        h_change = item[3]

        # for the d_change use item[4]
        d_change = item[4]

        # for trader_price use item[5]
        trader_price = item[5][0].text.split('\\')[0]

        # for the trader_name use item[6]
        trader_name = item[6][0].text

        # print(str(intX + 1) +
        #       " : " + str(name) +
        #       ' | ' + unsigned + " ₽" +
        #       ' | ' + str(slot_price) + " ₽" +
        #       ' | ' + h_change +
        #       ' | ' + d_change +
        #       ' | ' + trader_name +
        #       ' | ' + trader_price + " ₽")

        refined_values = (str(name),
                          unsigned + " ₽",
                          str(slot_price) + " ₽",
                          h_change,
                          d_change,
                          trader_name,
                          trader_price + " ₽")

        return refined_values
