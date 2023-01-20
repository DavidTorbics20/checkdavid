"""Everything that happens behind the scenes is in here.
   The website I will be gettint the flight information from
   is kiwi.com . Why? Because the url is simple and the gui
   library I use is also called kiwi (kivy)."""

import os
import re
import urllib.request
from datetime import datetime
import requests

import cfscrape
import requests
from bs4 import BeautifulSoup as BS


class Downloader():
    def __init__(self, url) -> None:
        self.url = url

    def get_page_content(self):
        # scraper = cfscrape.create_scraper()
        response = requests.get(self.url)
        # print(response.content)
        soup = BS(response.text, 'html.parser')
        # print(soup.prettify())

        alldivs = self.find_divs(soup)
        for div in alldivs:
            print(div)

    def find_divs(self, soup):
        mydivs = soup.find_all("time")  # noqa: E501
        return mydivs
