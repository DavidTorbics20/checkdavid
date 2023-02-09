"""Test the functionality of downloader.py."""

from bs4 import BeautifulSoup as BS
from src.downloader import Downloader
import parse


def test_download_01_downloader_exists():
    """Test if the Downloader class is implemented."""
    assert Downloader


def test_download_02_download_worked():
    """Test if the the website is really downloaded.
    A new file will appear called webpage.html and the title of it
    should be: "Tarkov - flea market - Keys - prices - Tarkov Market"
    """
    expected_title = "Tarkov - flea market - Keys - prices - Tarkov Market"
    # downloader = Downloader("tag/keys/")
    # downloader.get_page_content()
    with open('webpage_for_testing.html', 'r') as file:
        soup = BS(file.read(), 'html.parser')
        title = soup.find('title').text
    assert expected_title == title


def test_download_03_extracting_and_refining_from_file():
    downloader = Downloader("tag/keys/")
    results = downloader.extract_values("webpage_for_testing.html")

    test_item_nr_one = [
        'Zmeevsky 3 apartment 8 key',
        '23,622\\xe2\\x82\\xbd',
        [],
        '+260%',
        '+363%',
        '9,029\\xe2\\x82\\xbd',
        'Therapist'
    ]

    results = list(zip(results))[0]
    name = parse.parse("{'class': 'item-img', 'data-v-4e0a3d14': ''," +
                       " 'href': '{}', 'title': '{}'}",
                       str(results[0][0].__str__()).replace("\\", ""))

    assert test_item_nr_one[0] == name[1]
    assert test_item_nr_one[1] == results[0][1]
    assert test_item_nr_one[2] == results[0][2]
    assert test_item_nr_one[3] == results[0][3]
    assert test_item_nr_one[4] == results[0][4]
    assert test_item_nr_one[5] == results[0][5][0].text
    assert test_item_nr_one[6] == results[0][6][0].text
