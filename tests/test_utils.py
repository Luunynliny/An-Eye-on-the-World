from bs4 import BeautifulSoup

from src.utils import get_soup


def test_get_soup():
    with open("examplecom_response.txt", "r") as f:
        text = f.read()

    soup = get_soup("https://example.com")

    assert isinstance(soup, BeautifulSoup)
    assert BeautifulSoup(text, "html.parser") == soup
