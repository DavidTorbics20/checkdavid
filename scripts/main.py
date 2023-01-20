"""Main file."""

from downloader import Downloader


if __name__ == "__main__":
    url = "https://www.kiwi.com/en/search/results/vienna-austria/barcelona-spain/2023-02-20/2023-02-26/"
    downloader = Downloader(url)
    downloader.get_page_content()
