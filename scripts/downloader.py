"""Everything that happens behind the scenes is in here.
   The website I will be gettint the flight information from
   is kiwi.com . Why? Because the url is simple and the gui
   library I use is also called kiwi (kivy)."""

import os
import re
import urllib.request
from datetime import datetime

import cfscrape
import requests
from bs4 import BeautifulSoup as BS


class Downloader():
    def __init__(self, url) -> None:
        self.url = url

    def get_page_content(self):
        scraper = cfscrape.create_scraper()
        response = scraper.get(self.url)
        soup = BS(response.content, 'html.parser')

        alldivs = self.find_divs(soup)
        for div in alldivs:
            print(div)

    def find_divs(self, soup):
        mydivs = soup.find_all("div", {"class": "ResultCardcommonstyled_" +
                                                "_ResultCardWrapperCommo" +
                                                "n-sc-151jp81-1 ResultCa" +
                                                "rdstyled__ResultCardWra" +
                                                "pper-sc-vsw8q3-1 kHQVIh" +
                                                " hXywJo"})
        return mydivs
