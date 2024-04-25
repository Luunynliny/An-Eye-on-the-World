import requests
from bs4 import BeautifulSoup


def get_soup(url: str) -> BeautifulSoup:
    """
    Create a BeautifulSoup object from a URL.

    Args:
        url (str): URL to parse.

    Returns:
        BeautifulSoup: BeautifulSoup object.
    """
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')
