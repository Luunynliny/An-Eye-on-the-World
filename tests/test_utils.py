import bs4.element
import pytest
from bs4 import BeautifulSoup

from src.utils import get_soup, get_non_abrogated_articles

DATE: str = "2024-04-20"
CODE_CIVIL_URL: str = "https://www.legifrance.gouv.fr/codes/texte_lc/LEGITEXT000006070721"


@pytest.fixture()
def soup():
    return get_soup(CODE_CIVIL_URL + "/" + DATE)


def test_get_soup():
    with open("examplecom_response.txt", "r") as f:
        text = f.read()

    soup = get_soup("https://example.com")

    assert isinstance(soup, BeautifulSoup)
    assert BeautifulSoup(text, "html.parser") == soup


def test_get_non_abrogated_articles(soup):
    non_abrogated_articles = get_non_abrogated_articles(soup)

    assert isinstance(non_abrogated_articles, bs4.element.ResultSet)
    assert len(non_abrogated_articles) == 2883
