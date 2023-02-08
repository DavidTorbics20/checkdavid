"""Test the functionality of downloader.py."""

from bs4 import BeautifulSoup as BS
import scripts


def test_download_01_downloader_exists():
    """Test if the Downloader class is implemented."""
    assert scripts
    assert scripts.Downloader


def test_download_02_download_worked():
    """Test if the the website is really downloaded.

    A new file will appear called webpage.html and the title of it
    should be: "Tarkov - flea market - Keys - prices - Tarkov Market"
    """
    expected_title = "Tarkov - flea market - Keys - prices - Tarkov Market"

    downloader = scripts.Downloader("tag/keys/")
    downloader.get_page_content()

    with open('webpage.html', 'r') as file:
        soup = BS(file.read(), 'html.parser')
        title = soup.find('title')

    assert expected_title == title
