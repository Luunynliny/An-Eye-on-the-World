import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_soup(url: str) -> BeautifulSoup:
    """
    Create a BeautifulSoup object from a URL.

    Args:
        url (str): URL to parse.

    Returns:
        BeautifulSoup: BeautifulSoup object.
    """
    # Rotating proxies
    ua = UserAgent()

    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)

    # ic(response.text)

    return BeautifulSoup(response.text, 'html.parser')
