"""Main file."""

from downloader import Downloader


if __name__ == "__main__":
    url_extension = "ammo"
    url_extension = "tactical_devices"
    url_extension = "weapon"
    url_extension = "maps"
    url_extension = "weapon_parts"
    url_extension = ""
    url_extension = "tag/containers"
    url_extension = "tag/provisions"
    url_extension = "tag/magazines"
    downloader = Downloader(url_extension)
    downloader.get_page_content()
    extracted_valued = downloader.extract_values()
    a = downloader.get_values_from_extraction(extracted_valued)
